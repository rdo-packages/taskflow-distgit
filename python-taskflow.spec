%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%if 0%{?fedora}
%global with_python3 1
%endif

%global pypi_name taskflow

Name:           python-%{pypi_name}
Version:        XXX
Release:        XXX
Summary:        Taskflow structured state management library

License:        ASL 2.0
URL:            https://launchpad.net/taskflow
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz
BuildArch:      noarch

%description
A library to do [jobs, tasks, flows] in a HA manner using
different backends to be used with OpenStack projects.


%package -n python2-%{pypi_name}
Summary:        Taskflow structured state management library
BuildRequires:  python2-devel
BuildRequires:  python-pbr
BuildRequires:  git

Requires:       python-six
Requires:       python-babel
Requires:       python-stevedore
Requires:       python-futures
Requires:       python-networkx-core
Requires:       python-oslo-serialization >= 1.10.0
Requires:       python-oslo-utils >= 3.18.0
Requires:       python-jsonschema
Requires:       python-enum34
Requires:       python-debtcollector
Requires:       python-automaton >= 0.5.0
Requires:       python-networkx >= 1.10
Requires:       python-futurist >= 0.11.0
Requires:       python-fasteners >= 0.7
Requires:       python-tenacity >= 3.2.1
Requires:       python-contextlib2 >= 0.4.0
Requires:       python-cachetools >= 1.1.0

%{?python_provide:%python_provide python2-%{pypi_name}}

%description -n python2-%{pypi_name}
A library to do [jobs, tasks, flows] in a HA manner using
different backends to be used with OpenStack projects.

%if 0%{?with_python3}
%package -n python3-%{pypi_name}
Summary:        Taskflow structured state management library
BuildRequires:  python3-devel
BuildRequires:  python3-pbr

Requires:       python3-six
Requires:       python3-babel
Requires:       python3-stevedore
Requires:       python3-networkx-core
Requires:       python3-oslo-serialization >= 1.10.0
Requires:       python3-oslo-utils >= 3.18.0
Requires:       python3-jsonschema
Requires:       python3-enum34
Requires:       python3-debtcollector
Requires:       python3-automaton >= 0.5.0
Requires:       python3-networkx >= 1.10
Requires:       python3-futurist >= 0.11.0
Requires:       python3-fasteners >= 0.7
Requires:       python3-tenacity >= 3.2.1
Requires:       python3-contextlib2 >= 0.4.0
Requires:       python3-cachetools >= 1.1.0

%{?python_provide:%python_provide python3-%{pypi_name}}


%description -n python3-%{pypi_name}
A library to do [jobs, tasks, flows] in a HA manner using
different backends to be used with OpenStack projects.
%endif


%package doc
Summary:          Documentation for Taskflow
BuildRequires:  python-openstackdocstheme
BuildRequires:  python-oslo-sphinx
BuildRequires:  python-sphinx
BuildRequires:  python-oslo-utils
BuildRequires:  python-stevedore
BuildRequires:  python-enum34
BuildRequires:  python-oslo-serialization
BuildRequires:  python-futurist
BuildRequires:  python-fasteners
BuildRequires:  python-contextlib2
BuildRequires:  python-jsonschema
BuildRequires:  python-automaton
BuildRequires:  python-kombu
BuildRequires:  python-networkx
BuildRequires:  python-kazoo
BuildRequires:  python-redis
BuildRequires:  python-cachetools
BuildRequires:  python-tenacity
BuildRequires:  python-alembic
BuildRequires:  python-sqlalchemy-utils



%description doc
A library to do [jobs, tasks, flows] in a HA manner using
different backends to be used with OpenStack projects.
This package contains the associated documentation.

%prep
%autosetup -n %{pypi_name}-%{upstream_version} -S git
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
