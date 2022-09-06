%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global pypi_name taskflow

%global with_doc 1

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
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif
BuildArch:      noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
BuildRequires:  openstack-macros
%endif

%description
%{common_desc}


%package -n python3-%{pypi_name}
Summary:        Taskflow structured state management library
%{?python_provide:%python_provide python3-%{pypi_name}}
BuildRequires:  python3-devel
BuildRequires:  python3-pbr
BuildRequires:  git-core
BuildRequires:  python3-babel
BuildRequires:  openstack-macros

Requires:       python3-cachetools >= 2.0.0
Requires:       python3-jsonschema
Requires:       python3-stevedore
Requires:       python3-oslo-serialization >= 2.18.0
Requires:       python3-oslo-utils >= 3.33.0
Requires:       python3-automaton >= 1.9.0
Requires:       python3-futurist >= 1.2.0
Requires:       python3-fasteners >= 0.17.3
Requires:       python3-pbr >= 2.0.0
Requires:       python3-tenacity >= 6.0.0
Requires:       python3-pydot >= 1.2.4
Requires:       python3-networkx >= 2.1.0

%description -n python3-%{pypi_name}
%{common_desc}

%if 0%{?with_doc}
%package doc
Summary:          Documentation for Taskflow
BuildRequires:  python3-alembic
BuildRequires:  python3-cachetools
BuildRequires:  python3-jsonschema
BuildRequires:  python3-openstackdocstheme
BuildRequires:  python3-sphinx
BuildRequires:  graphviz
BuildRequires:  python3-oslo-utils
BuildRequires:  python3-stevedore
BuildRequires:  python3-oslo-serialization
BuildRequires:  python3-futurist
BuildRequires:  python3-fasteners
BuildRequires:  python3-automaton
BuildRequires:  python3-kombu
BuildRequires:  python3-tenacity

BuildRequires:  python3-redis
BuildRequires:  python3-kazoo
BuildRequires:  python3-networkx
BuildRequires:  python3-sqlalchemy-utils

%description doc
%{common_desc}

This package contains the associated documentation.
%endif

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{pypi_name}-%{upstream_version} -S git

# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
%py_req_cleanup


%build
%{py3_build}

%if 0%{?with_doc}
# generate html docs
sphinx-build-3 -b html doc/source doc/build/html
# remove the sphinx-build-3 leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%{py3_install}

%files -n python3-%{pypi_name}
%doc README.rst
%license LICENSE
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-*.egg-info

%if 0%{?with_doc}
%files doc
%doc doc/build/html
%license LICENSE
%endif

%changelog
