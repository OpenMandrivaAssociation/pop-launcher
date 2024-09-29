
Name:           pop-launcher
Version:        1.2.3+git20240814
Release:        0
Summary:        Modular IPC-based desktop launcher service
License:        MPL-2.0
URL:            https://github.com/pop-os/launcher
# get git clone --recursive https://github.com/pop-os/launcher
Source0:        https://github.com/pop-os/launcher/archive/launcher.tar.lz
Source1:        vendor.tar.xz
Patch0:         fix-justfile.patch

BuildRequires:	lzip
BuildRequires:  rust-packaging
BuildRequires:  just
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(xkbcommon)

Requires:  cosmic-launcher

%description
Modular IPC-based desktop launcher service, written in Rust. Desktop launchers
may interface with this service via spawning the pop-launcher process and
communicating to it via JSON IPC over the stdin and stdout pipes. The launcher
service will also spawn plugins found in plugin directories on demand, based on
the queries sent to the service.

Using IPC enables each plugin to isolate their data from other plugin processes
and frontends that are interacting with them. If a plugin crashes, the launcher
will continue functioning normally, gracefully cleaning up after the crashed
process. Frontends and plugins may also be written in any language. The
pop-launcher will do its part to schedule the execution of these plugins in
parallel, on demand.

%prep
%autosetup -n launcher -a1 -p1
mkdir .cargo
cp %{SOURCE2} .cargo/config


%build
export RUSTFLAGS="-C codegen-units=1"
just build-release

%install
just rootdir=%{buildroot} prefix=%{_prefix} install


%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_prefix}/lib/%{name}
