Summary:	Generate reports from various logfiles
Name:		lire
Version:	20010626
Release:	3
Source0:	http://logreport.org/pub/%{name}-%{version}.tar.gz
Source1:	%{name}.cron
Patch0:		%{name}-nopdftexdoc.patch
URL:		http://www.logreport.org/
License:	GPL
Group:		Applications/System
Group(de):	Applikationen/System
Group(pl):	Aplikacje/System
Vendor:		LogReport Foundation (http://www.logreport.org)
PreReq:		sh-utils, shadow-utils
Requires:	crondaemon
BuildRequires:	openjade, opensp, sgml-common, lynx, perl, perl-modules
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
BuildArchitectures:	noarch

%include	/usr/lib/rpm/macros.perl
%define		_sysconfdir		/etc/%{name}

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

%__gzip -9fn doc/*.txt

%install
%__rm -rf $RPM_BUILD_ROOT
%{__install} -d $RPM_BUILD_ROOT{%{_localstatedir}/spool/%{name},%{_localstatedir}/lib/%{name},/etc/cron.d}
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	sysconfdir=/etc \
	LR_PERL5LIBDIR=%perl_sitearch

%{__install} %{SOURCE1} $RPM_BUILD_ROOT/etc/cron.d/lire

%clean
%__rm -rf $RPM_BUILD_ROOT

%pre
if [ -n "`getgid lire`" ]; then
    /usr/sbin/groupadd -r -f lire
    if [ -n "`id -u lire 2>/dev/null`" ]; then
	/usr/sbin/useradd -r -c "Lire User" -d %{_localstatedir}/spool/%{name} lire
    fi
fi

%files
%defattr(644,root,root,755)
%doc README* INSTALL NEWS THANKS COPYING AUTHORS
%doc doc/*.txt.* doc/*.html doc/TODO doc/BUGS

%attr(640,root,root) %config /etc/cron.d/lire

%attr(775,root,lire) %dir %{_sysconfdir}
%attr(775,root,lire) %dir %{_sysconfdir}/apachemodgzip
%attr(775,root,lire) %dir %{_sysconfdir}/dns
%attr(775,root,lire) %dir %{_sysconfdir}/email
%attr(775,root,lire) %dir %{_sysconfdir}/www

%attr(664,root,lire) %config %{_sysconfdir}/address.cf
%attr(664,root,lire) %config %{_sysconfdir}/defaults
%attr(664,root,lire) %config %{_sysconfdir}/disclaimer
%attr(664,root,lire) %config %{_sysconfdir}/explanation
%attr(664,root,lire) %config %{_sysconfdir}/profile_lean
%attr(664,root,lire) %config %{_sysconfdir}/signature

%attr(664,root,lire) %config %{_sysconfdir}/*/*

%attr(755,root,root) %{_bindir}/*
%{_libexecdir}/%{name}
%{perl_sitearch}/Lire
%{_datadir}/%{name}

%attr(770,root,lire) %dir %{_localstatedir}/spool/%{name}
%attr(770,root,lire) %dir %{_localstatedir}/lib/%{name}

%doc %{_mandir}/man1/*.1*
%doc %{_mandir}/man3/*.3pm*
