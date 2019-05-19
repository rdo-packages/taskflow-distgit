# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
# End of macros for py2/py3 compatibility
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global pypi_name taskflow

%global with_doc 1

%global common_desc \
A library to do [jobs, tasks, flows] in a HA manner using \
different backends to be used with OpenStack projects.

Name:           python-%{pypi_name}
Version:        3.5.0
Release:        1%{?dist}
Summary:        Taskflow structured state management library

License:        ASL 2.0
URL:            https://launchpad.net/taskflow
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz
BuildArch:      noarch

%description
%{common_desc}


%package -n python%{pyver}-%{pypi_name}
Summary:        Taskflow structured state management library
%{?python_provide:%python_provide python%{pyver}-%{pypi_name}}
BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-pbr
BuildRequires:  git
BuildRequires:  python%{pyver}-babel
BuildRequires:  openstack-macros

Requires:       python%{pyver}-cachetools >= 2.0.0
Requires:       python%{pyver}-jsonschema
Requires:       python%{pyver}-six
Requires:       python%{pyver}-stevedore
Requires:       python%{pyver}-oslo-serialization >= 2.18.0
Requires:       python%{pyver}-oslo-utils >= 3.33.0
Requires:       python%{pyver}-debtcollector
Requires:       python%{pyver}-automaton >= 1.9.0
Requires:       python%{pyver}-futurist >= 1.2.0
Requires:       python%{pyver}-fasteners >= 0.7
Requires:       python%{pyver}-pbr >= 2.0.0
Requires:       python%{pyver}-tenacity >= 4.4.0

# Handle python2 exception
%if %{pyver} == 2
Requires:       python%{pyver}-contextlib2 >= 0.4.0
Requires:       python-enum34
Requires:       python-futures
Requires:       python-networkx >= 1.10
Requires:       python-networkx-core
%else
Requires:       python%{pyver}-networkx >= 1.10
Requires:       python%{pyver}-networkx-core
%endif

%description -n python%{pyver}-%{pypi_name}
%{common_desc}

%if 0%{?with_doc}
%package doc
Summary:          Documentation for Taskflow
BuildRequires:  python%{pyver}-alembic
BuildRequires:  python%{pyver}-cachetools
BuildRequires:  python%{pyver}-jsonschema
BuildRequires:  python%{pyver}-openstackdocstheme
BuildRequires:  python%{pyver}-sphinx
BuildRequires:  graphviz
BuildRequires:  python%{pyver}-oslo-utils
BuildRequires:  python%{pyver}-stevedore
BuildRequires:  python%{pyver}-oslo-serialization
BuildRequires:  python%{pyver}-futurist
BuildRequires:  python%{pyver}-fasteners
BuildRequires:  python%{pyver}-automaton
BuildRequires:  python%{pyver}-kombu
BuildRequires:  python%{pyver}-tenacity

# Handle python2 exception
%if %{pyver} == 2
BuildRequires:  python%{pyver}-contextlib2
BuildRequires:  python-enum34
BuildRequires:  python-redis
BuildRequires:  python-kazoo
BuildRequires:  python-networkx
BuildRequires:  python-sqlalchemy-utils
%else
BuildRequires:  python%{pyver}-redis
BuildRequires:  python%{pyver}-kazoo
BuildRequires:  python%{pyver}-networkx
BuildRequires:  python%{pyver}-sqlalchemy-utils
%endif

%description doc
%{common_desc}

This package contains the associated documentation.
%endif

%prep
%autosetup -n %{pypi_name}-%{upstream_version} -S git
# TODO(apevec) remove once python-networking subpackaging is fixed
sed -i /networkx.drawing/d taskflow/types/graph.py

# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
%py_req_cleanup


%build
%{pyver_build}

%if 0%{?with_doc}
# generate html docs
%{pyver_bin} setup.py build_sphinx -b html
# remove the sphinx-build-%{pyver} leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%{pyver_install}

%files -n python%{pyver}-%{pypi_name}
%doc README.rst
%license LICENSE
%{pyver_sitelib}/%{pypi_name}
%{pyver_sitelib}/%{pypi_name}-*.egg-info

%if 0%{?with_doc}
%files doc
%doc doc/build/html
%license LICENSE
%endif

%changelog
* Sun May 19 2019 RDO <dev@lists.rdoproject.org> 3.5.0-1
- Update to 3.5.0

* Tue Mar 12 2019 RDO <dev@lists.rdoproject.org> 3.4.0-1
- Update to 3.4.0

