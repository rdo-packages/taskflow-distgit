%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%if 0%{?fedora}
%global with_python3 1
%endif

%global pypi_name taskflow

# see https://fedoraproject.org/wiki/Packaging:Python#Macros
%if 0%{?rhel} && 0%{?rhel} <= 6
%{!?__python2: %global __python2 /usr/bin/python2}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python2_sitearch: %global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:           python-%{pypi_name}
Version:        1.30.0
Release:        2%{?dist}
Summary:        Taskflow structured state management library

License:        ASL 2.0
URL:            https://launchpad.net/taskflow
Source0:        http://pypi.python.org/packages/source/t/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

%description
A library to do [jobs, tasks, flows] in a HA manner using
different backends to be used with OpenStack projects.


%package -n python2-%{pypi_name}
Summary:        Taskflow structured state management library
BuildRequires:  python2-devel
BuildRequires:  python-pbr

Requires:       python-anyjson
Requires:       python-iso8601
Requires:       python-six
Requires:       python-babel
Requires:       python-stevedore
Requires:       python-futures
Requires:       python-networkx-core
Requires:       python-oslo-serialization
Requires:       python-oslo-utils
Requires:       python-jsonschema
Requires:       python-enum34
Requires:       python-debtcollector
Requires:       python-automaton >= 0.5.0
Requires:       python-networkx >= 1.10

%{?python_provide:%python_provide python2-%{pypi_name}}

%description -n python2-%{pypi_name}
A library to do [jobs, tasks, flows] in a HA manner using
different backends to be used with OpenStack projects.

%if 0%{?with_python3}
%package -n python3-%{pypi_name}
Summary:        Taskflow structured state management library
BuildRequires:  python3-devel
BuildRequires:  python3-pbr

Requires:       python3-anyjson
Requires:       python3-iso8601
Requires:       python3-six
Requires:       python3-babel
Requires:       python3-stevedore
Requires:       python3-futures
Requires:       python3-networkx-core
Requires:       python3-oslo-serialization
Requires:       python3-oslo-utils
Requires:       python3-jsonschema
Requires:       python3-enum34
Requires:       python3-debtcollector
Requires:       python3-automaton >= 0.5.0
Requires:       python3-networkx >= 1.10

%{?python_provide:%python_provide python3-%{pypi_name}}


%description -n python3-%{pypi_name}
A library to do [jobs, tasks, flows] in a HA manner using
different backends to be used with OpenStack projects.
%endif


%package doc
Summary:          Documentation for Taskflow
BuildRequires:  python-oslo-sphinx
BuildRequires:  python-sphinx


%description doc
A library to do [jobs, tasks, flows] in a HA manner using
different backends to be used with OpenStack projects.
This package contains the associated documentation.

%prep
%setup -q -n %{pypi_name}-%{upstream_version}
# TODO(apevec) remove once python-networking subpackaging is fixed
sed -i /networkx.drawing/d taskflow/types/graph.py

# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
rm -rf {test-,}requirements.txt


%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif
# generate html docs
%if 0%{?rhel} == 6
sphinx-1.0-build doc/source html
%else
sphinx-build doc/source html
%endif
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}


%install
%py2_install
%if 0%{?with_python3}
%py3_install
%endif


%files -n python2-%{pypi_name}
%doc README.rst
%license LICENSE
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/%{pypi_name}-*.egg-info

%if 0%{?with_python3}
%files -n python3-%{pypi_name}
%doc README.rst
%license LICENSE
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-*.egg-info
%endif

%files doc
%doc html
%license LICENSE

%changelog
* Fri May 06 2016 Alan Pevec <apevec AT redhat.com> - 1.30.0-2
- Added python-networkx missing packages
- Remove dependency on networkx.drawing

* Wed Mar 23 2016 Haikel Guemar <hguemar@fedoraproject.org> 1.30.0-
- Update to 1.30.0

