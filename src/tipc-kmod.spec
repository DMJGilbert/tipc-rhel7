%define kmod_name		tipc

#%{!?dist: %define dist .el6}
#%{!?kernel_version: %global kernel_version %(uname -r)}

Source0:	tipc.tar.bz2
Source1:	tipc.conf
Source10:	tipc-kmodtool.sh
Name:           %{kmod_name}
Version:        2.0
Release:        1.0%{?dist}
Group:          System Environment/Kernel
License:        Dual BSD/GPL
Summary:        TIPC: Transparent Inter Process Communication
URL:            http://tipc.sourceforge.net
BuildRequires:  %kernel_module_package_buildreqs kabi-whitelists
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
ExclusiveArch:  i686 x86_64

%files
%defattr(-,root,root,-)
/etc/depmod.d/tipc.conf


#Because redhat-rpm-config is hopelessly broken in chroot environments
%define kversion %{expand:%(sh %{SOURCE10} verrel)}
%{expand:%(sh %{SOURCE10} rpmtemplate %{kmod_name} %{kversion} "")}

%define debug_package %{nil}

%description
This package provides a TIPC stack with additional upstream patches.
It is built to depend upon the specific ABI provided by a range of releases
of the same variant of the Linux kernel and not on any one specific build.

%prep
%setup -n %{kmod_name}
set -- *
mkdir tipc
mv "$@" tipc/
%{echo:prep stage 2}
echo "override %{kmod_name} * weak-updates/%{kmod_name}" > %{kmod_name}.conf

%build
ksrc="%{_usrsrc}/kernels/%{kversion}"
%{__make} -C "$ksrc" %{?_smp_mflags} CONFIG_TIPC=m TIPC_PORTS=131072 M=$PWD/tipc

%install
%{__install} -d %{buildroot}/lib/modules/%{kversion}/extra/%{kmod_name}/
%{__install} $PWD/tipc/*.ko %{buildroot}/lib/modules/%{kversion}/extra/%{kmod_name}/
%{__install} -d %{buildroot}%{_sysconfdir}/depmod.d/
%{__install} %{kmod_name}.conf %{buildroot}%{_sysconfdir}/depmod.d/
%{__rm} -f %{buildroot}/lib/modules/%{kversion}/modules.*

%clean
%{__rm} -rf %{buildroot}

%changelog
* Mon Jan 27 2014 Erik Hugne <erik.hugne@ericsson.com>
- Large portions rewritten due to chroot related bugs
  in redhat-rpm-config

* Fri Nov 22 2013 Erik Hugne <erik.hugne@ericsson.com>
- Initial version


