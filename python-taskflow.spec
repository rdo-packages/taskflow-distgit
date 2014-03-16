# Created by pyp2rpm-1.0.1
%global pypi_name taskflow

# see https://fedoraproject.org/wiki/Packaging:Python#Macros
%if 0%{?rhel} && 0%{?rhel} <= 6
%{!?__python2: %global __python2 /usr/bin/python2}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python2_sitearch: %global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

Name:           python-%{pypi_name}
Version:        0.1.2
Release:        5%{?dist}
Summary:        Taskflow structured state management library

License:        ASL 2.0
URL:            https://launchpad.net/taskflow
Source0:        http://pypi.python.org/packages/source/t/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-pbr
%if 0%{?rhel} == 6
BuildRequires:  python-sphinx10
%else
BuildRequires:  python-sphinx
%endif

Requires:       python-anyjson
Requires:       python-iso8601
Requires:       python-six
Requires:       python-babel
Requires:       python-stevedore
Requires:       python-futures
Requires:       python-networkx-core

%description
A library to do [jobs, tasks, flows] in a HA manner using
different backends to be used with OpenStack projects.

%package doc
Summary:          Documentation for OpenStack Compute
Group:            Documentation

%description doc
A library to do [jobs, tasks, flows] in a HA manner using
different backends to be used with OpenStack projects.
This package contains the associated documentation.

%prep
%setup -q -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
rm -rf {test-,}requirements.txt


%build
%{__python2} setup.py build


%install
%{__python2} setup.py install --skip-build --root %{buildroot}

# generate html docs
%if 0%{?rhel} == 6
sphinx-1.0-build doc html
%else
sphinx-build doc html
%endif
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}


%files
%doc README.md LICENSE
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info

%files doc
%doc html

%changelog
* Sun Mar 16 2014 Padraig Brady <P@draigBrady.com> - 0.1.2-5
- Reduce dependency to python-networkx-core subpackage

* Wed Jan 29 2014 Padraig Brady <P@draigBrady.com> - 0.1.2-4
- Initial package.
