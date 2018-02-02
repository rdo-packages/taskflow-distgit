%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%if 0%{?fedora}
%global with_python3 1
%endif

%global pypi_name taskflow

%global common_desc \
A library to do [jobs, tasks, flows] in a HA manner using \
different backends to be used with OpenStack projects.

Name:           python-%{pypi_name}
Version:        XXX
Release:        XXX
Summary:        Taskflow structured state management library

License:        ASL 2.0
URL:            https://launchpad.net/taskflow
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz
BuildArch:      noarch

%description
%{common_desc}


%package -n python2-%{pypi_name}
Summary:        Taskflow structured state management library
BuildRequires:  python2-devel
BuildRequires:  python2-pbr
BuildRequires:  git
BuildRequires:  python2-babel
BuildRequires:  openstack-macros

Requires:       python2-cachetools >= 2.0.0
Requires:       python2-futures
Requires:       python2-jsonschema
Requires:       python2-six
Requires:       python2-stevedore
Requires:       python2-oslo-serialization >= 2.18.0
Requires:       python2-oslo-utils >= 3.33.0
Requires:       python2-debtcollector
Requires:       python2-automaton >= 1.9.0
Requires:       python2-futurist >= 1.2.0
Requires:       python2-fasteners >= 0.7
Requires:       python2-tenacity >= 3.2.1
%if 0%{?fedora} > 0
Requires:       python2-enum34
Requires:       python2-contextlib2 >= 0.4.0
Requires:       python2-networkx >= 1.10
Requires:       python2-networkx-core
%else
Requires:       python-enum34
Requires:       python-contextlib2 >= 0.4.0
Requires:       python-networkx >= 1.10
Requires:       python-networkx-core
%endif

%{?python_provide:%python_provide python2-%{pypi_name}}

%description -n python2-%{pypi_name}
%{common_desc}

%if 0%{?with_python3}
%package -n python3-%{pypi_name}
Summary:        Taskflow structured state management library
BuildRequires:  python3-devel
BuildRequires:  python3-pbr
BuildRequires:  python3-babel

Requires:       python3-six
Requires:       python3-stevedore
Requires:       python3-networkx-core
Requires:       python3-oslo-serialization >= 2.18.0
Requires:       python3-oslo-utils >= 3.33.0
Requires:       python3-jsonschema
Requires:       python3-enum34
Requires:       python3-debtcollector
Requires:       python3-automaton >= 1.9.0
Requires:       python3-networkx >= 1.10
Requires:       python3-futurist >= 1.2.0
Requires:       python3-fasteners >= 0.7
Requires:       python3-tenacity >= 3.2.1
Requires:       python3-contextlib2 >= 0.4.0
Requires:       python3-cachetools >= 2.0.0

%{?python_provide:%python_provide python3-%{pypi_name}}


%description -n python3-%{pypi_name}
%{common_desc}
%endif


%package doc
Summary:          Documentation for Taskflow
BuildRequires:  python2-alembic
BuildRequires:  python2-cachetools
BuildRequires:  python2-jsonschema
BuildRequires:  python2-openstackdocstheme
BuildRequires:  python2-sphinx
BuildRequires:  graphviz
BuildRequires:  python2-oslo-utils
BuildRequires:  python2-stevedore
BuildRequires:  python2-oslo-serialization
BuildRequires:  python2-futurist
BuildRequires:  python2-fasteners
BuildRequires:  python2-automaton
BuildRequires:  python2-kombu
BuildRequires:  python2-tenacity
%if 0%{?fedora} > 0
BuildRequires:  python2-enum34
BuildRequires:  python2-contextlib2
BuildRequires:  python2-redis
BuildRequires:  python2-kazoo
BuildRequires:  python2-networkx
BuildRequires:  python2-sqlalchemy-utils
%else
BuildRequires:  python-enum34
BuildRequires:  python-contextlib2
BuildRequires:  python-redis
BuildRequires:  python-kazoo
BuildRequires:  python-networkx
BuildRequires:  python-sqlalchemy-utils
%endif


%description doc
%{common_desc}

This package contains the associated documentation.

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
%py2_build
%if 0%{?with_python3}
%py3_build
%endif
# generate html docs
%{__python2} setup.py build_sphinx -b html
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}


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
%doc doc/build/html
%license LICENSE

%changelog
