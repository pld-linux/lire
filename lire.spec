Summary:	Generate reports from various logfiles
Name:		lire
Version:	20010626
Release:	3
License:	GPL
Vendor:		LogReport Foundation (http://www.logreport.org)
Group:		Applications/System
Group(de):	Applikationen/System
Group(pl):	Aplikacje/System
Source0:	http://logreport.org/pub/%{name}-%{version}.tar.gz
Source1:	%{name}.cron
Patch0:		%{name}-nopdftexdoc.patch
URL:		http://www.logreport.org/
PreReq:		sh-utils, shadow-utils
Requires:	crondaemon
BuildRequires:	openjade, opensp, sgml-common, lynx, perl, perl-modules
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%include	/usr/lib/rpm/macros.perl

%description
Lire automatically generates useful reports from raw logfiles from
various services. Currently, exim, sendmail, qmail, postfix, bind, boa
and some apache logfiles are supported.

Reports are in ASCII, PDF or HTML format. Logs can be read from the
local system in a cronjob, or can be received via email.

If you're not running any of the supported services, this package
won't be very useful for you.

%prep
%setup -q
%patch0 -p1

%build
HASXALAN=no \
LR_PERL5LIBDIR=%perl_sitearch \
LR_SPOOLDIR=%{_localstatedir}/spool/%{name} \
LR_ARCHIVEDIR=%{_localstatedir}/lib/%{name}
%{__autoconf}
%configure
%{__make}

%install
%{__rm} -rf $RPM_BUILD_ROOT
%{__install} -d $RPM_BUILD_ROOT{%{_localstatedir}/spool/%{name},%{_localstatedir}/lib/%{name},/etc/cron.d}
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	LR_PERL5LIBDIR=%perl_sitearch

%{__install} %{SOURCE1} $RPM_BUILD_ROOT/etc/cron.d/lire

%clean
%__rm -rf $RPM_BUILD_ROOT

%__gzip -9fn doc/*.txt README* NEWS THANKS AUTHORS \
	doc/TODO doc/BUGS

%pre
%groupadd
COMMENT="Lire User"; HOMEDIR="%{_localstatedir}/spool/%{name}"; %useradd

%postun
%userdel
%groupdel

%files
%defattr(644,root,root,755)
%doc *.gz doc/*gz doc/*.html

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
%{perl_sitearch}/Lire
%{_datadir}/%{name}

%attr(770,root,lire) %dir %{_localstatedir}/spool/%{name}
%attr(770,root,lire) %dir %{_localstatedir}/lib/%{name}

%{_mandir}/man1/*.1*
%{_mandir}/man3/*.3pm*
