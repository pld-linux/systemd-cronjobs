Summary:	crond-like services for systemd
Summary(pl.UTF-8):	Usługi typu crond dla systemd
Name:		systemd-cronjobs
Version:	0.1
Release:	1
License:	GPL v2
Group:		Base
Source0:	cronjobs.target
Source1:	cronjob-hourly.timer
Source2:	cronjob-hourly.service
Source3:	cronjob-daily.timer
Source4:	cronjob-daily.service
Source5:	cronjob-weekly.timer
Source6:	cronjob-weekly.service
Source7:	cronjob-monthly.timer
Source8:	cronjob-monthly.service
Source9:	README
URL:		http://pld-linux.org/
Requires:	systemd-init
Provides:	cronjobs
Provides:	group(crontab)
Obsoletes:	crondaemon
Obsoletes:	cronjobs
Obsoletes:	crontabs
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
crond-like services for systemd.

%description -l pl.UTF-8
Usługi typu crond dla systemd.

%prep
%setup -q -cT

%build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{systemdunitdir} \
	$RPM_BUILD_ROOT%{_sysconfdir}/cron.{hourly,daily,weekly,monthly}

cp -p %{SOURCE0} %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4} \
	%{SOURCE5} %{SOURCE6} %{SOURCE7} %{SOURCE8} \
	$RPM_BUILD_ROOT%{systemdunitdir}

cp -p %{SOURCE9} .

%post
# the message displayed by systemd_post would be misleading
# onlyt cronjobs.target needs to be started manually
export SYSTEMD_LOG_LEVEL=warning SYSTEMD_LOG_TARGET=syslog
/bin/systemd_booted && /bin/systemctl --quiet daemon-reload || :
/bin/systemctl preset --preset-mode=enable-only cronjob-hourly.timer cronjob-daily.timer cronjob-weekly.timer cronjob-monthly.timer cronjobs.target
/bin/systemd_booted && echo 'Run "/bin/systemctl start cronjobs.target" to start systemd cron jobs.' || :

%pre
%groupadd -g 117 -r -f crontab

%preun
%systemd_preun cronjob-hourly.timer cronjob-daily.timer cronjob-weekly.timer cronjob-monthly.timer cronjobs.target

%postun
if [ "$1" = "0" ]; then
	%groupremove crontab
fi
%systemd_reload

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README
%attr(750,root,crontab) %dir /etc/cron.daily
%attr(750,root,crontab) %dir /etc/cron.hourly
%attr(750,root,crontab) %dir /etc/cron.monthly
%attr(750,root,crontab) %dir /etc/cron.weekly
%{systemdunitdir}/cronjobs.target
%{systemdunitdir}/cronjob-*.timer
%{systemdunitdir}/cronjob-*.service
