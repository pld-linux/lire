Summary:	Generate reports from various logfiles
Summary(pl.UTF-8):	Generator raportów z różnych logów
Name:		lire
Version:	1.3
Release:	2
Epoch:		1
License:	GPL
Vendor:		LogReport Foundation (http://www.logreport.org)
Group:		Applications/System
Source0:	http://logreport.org/pub/lire-%{version}.tar.gz
# Source0-md5:	62f16cfd1554fc3485d0e88f0c37b8b4
Source1:	%{name}.cron
Patch0:		%{name}-nopdftexdoc.patch
Patch1:		%{name}-am.patch
URL:		http://www.logreport.org/
BuildConflicts:	openjade, libxslt-progs
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	lynx
BuildRequires:	opensp
BuildRequires:	perl-devel
BuildRequires:	rpm-perlprov
BuildRequires:	rpmbuild(macros) >= 1.202
BuildRequires:	sgml-common
BuildRequires:	smtpdaemon
Prereq:		coreutils
Prereq:		shadow-utils
Requires:	crondaemon
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Provides:	group(lire)
Provides:	user(lire)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
BuildArch:	noarch

%description
Lire automatically generates useful reports from raw logfiles from
various services. Currently, exim, sendmail, qmail, postfix, bind, boa
and some apache logfiles are supported.

Reports are in ASCII, PDF or HTML format. Logs can be read from the
local system in a cronjob, or can be received via email.

If you're not running any of the supported services, this package
won't be very useful for you.

%description -l pl.UTF-8
Lire automatycznie generuje użyteczne raporty z surowych plików logów
różnych serwisów. Aktualnie obsługiwane są logi: exima, sendmaila,
qmaila, postfiksa, binda, boa, apache.

Raporty mogą być w formacie ASCII, PDF lub HTML. Logi mogą być czytane
z lokalnego systemu z crona lub dostarczane e-mailem.

%prep
%setup -q
#%patch0 -p1
%patch -P1 -p0

# ugly kludge, but I don't know the proper way
find -type f | xargs %{__perl} -pi -e 's/^all: all-redirect/all: /'

%build
%{__aclocal}
%{__autoconf}
#%{__autoheader}
%{__automake}
%configure \
	--with-spooldir=%{_localstatedir}/spool/%{name} \
	--with-perl5libdir=%{perl_vendorlib} \
	--with-perl5archlibdir=%{perl_vendorarch} \
	--with-archivedir=%{_localstatedir}/lib/%{name}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_localstatedir}/spool/%{name},%{_localstatedir}/lib/%{name},/etc/cron.d}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	LR_PERL5LIBDIR=%{perl_vendorlib}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/cron.d/lire

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 106 lire
%useradd -u 106 -c "Lire User" -d %{_localstatedir}/spool/%{name} -g lire lire

%postun
if [ "$1" = "0" ]; then
	%userremove lire
	%groupremove lire
fi

%files
%defattr(644,root,root,755)
%doc doc/*.txt README* NEWS THANKS AUTHORS doc/TODO doc/BUGS
%attr(640,root,root) %config /etc/cron.d/lire
%attr(775,root,lire) %dir %{_sysconfdir}/%{name}
%attr(775,root,lire) %dir %{_sysconfdir}/%{name}/apachemodgzip
%attr(775,root,lire) %dir %{_sysconfdir}/%{name}/dns
%attr(775,root,lire) %dir %{_sysconfdir}/%{name}/email
%attr(775,root,lire) %dir %{_sysconfdir}/%{name}/www
%attr(664,root,lire) %config %{_sysconfdir}/%{name}/address.cf
%attr(664,root,lire) %config %{_sysconfdir}/%{name}/defaults
%attr(664,root,lire) %config %{_sysconfdir}/%{name}/disclaimer
%attr(664,root,lire) %config %{_sysconfdir}/%{name}/explanation
%attr(664,root,lire) %config %{_sysconfdir}/%{name}/profile_lean
%attr(664,root,lire) %config %{_sysconfdir}/%{name}/signature
%attr(664,root,lire) %config %{_sysconfdir}/%{name}/*/*
%attr(755,root,root) %{_bindir}/*
%{_libexecdir}/%{name}
%{perl_vendorlib}/Lire
%{_datadir}/%{name}
%attr(770,root,lire) %dir %{_localstatedir}/spool/%{name}
%attr(770,root,lire) %dir %{_localstatedir}/lib/%{name}
%{_mandir}/man1/*.1*
%{_mandir}/man3/*.3pm*
