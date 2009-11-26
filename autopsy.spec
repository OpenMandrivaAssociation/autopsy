%define _provides_exceptions perl(Appsort)\\|perl(Appview)\\|perl(Args)\\|perl(Caseman)\\|perl(Data)\\|perl(Exec)\\|perl(File)\\|perl(Filesystem)\\|perl(Frame)\\|perl(Fs)\\|perl(Hash)\\|perl(Kwsrch)\\|perl(Main)\\|perl(Meta)\\|perl(Notes)\\|perl(Print)\\|perl(Timeline)\\|perl(autopsyfunc)\\|perl(conf.pl)\\|perl(define.pl)\\|perl(fs.pl)\\|perl(search.pl)
%define _requires_exceptions perl(Appsort)\\|perl(Appview)\\|perl(Args)\\|perl(Caseman)\\|perl(Data)\\|perl(Exec)\\|perl(File)\\|perl(Filesystem)\\|perl(Frame)\\|perl(Fs)\\|perl(Hash)\\|perl(Kwsrch)\\|perl(Main)\\|perl(Meta)\\|perl(Notes)\\|perl(Print)\\|perl(Timeline)\\|perl(autopsyfunc)\\|perl(conf.pl)\\|perl(define.pl)\\|perl(fs.pl)\\|perl(search.pl)

Summary:	Autopsy Forensic Browser
Name:		autopsy
Version:	2.21
Release:	%mkrel 3
License:	GPLv2+
Group:		System/Base
URL:		http://www.sleuthkit.org
Source0:	http://dfn.dl.sourceforge.net/sourceforge/autopsy/%name-%version.tar.gz
Requires:	binutils
Requires:	file
Requires:	grep
Requires:	perl
Requires:	sleuthkit >= 1.61
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-root

%description
The Autopsy Forensic Browser is a graphical interface to the command line
digital forensic analysis tools in The Sleuth Kit. Together, The Sleuth Kit and
Autopsy provide many of the same features as commercial digital forensics tools
for the analysis of Windows(tm) and UNIX file systems (NTFS, FAT, FFS, EXT2FS,
and EXT3FS).

The Sleuth Kit and Autopsy are both Open Source and run on UNIX platforms. As
Autopsy is HTML-based, the investigator can connect to the Autopsy server from
any platform using an HTML browser. Autopsy provides a "File Manager"-like
interface and shows details about deleted data and file system structures.

%prep

%setup -q

%build

# "build" autopsy
cat > autopsy << EOF
#!%{_bindir}/perl -wT
use lib '%{_datadir}/autopsy/';
use lib '%{_datadir}/autopsy/lib/';
EOF
cat base/autopsy.base >> autopsy

# "build" make-live-cd
cat > make-live-cd << EOF
#!%{_bindir}/perl
use lib '%{_datadir}/autopsy/';
use lib '%{_datadir}/autopsy/lib/';
EOF
cat base/make-live-cd.base >> make-live-cd

# "build" conf.pl
cat > conf.pl << EOF
# Autopsy configuration settings

# when set to 1, the server will stop after it receives no
# connections for STIMEOUT seconds. 
\$USE_STIMEOUT = 0;
\$STIMEOUT = 3600;

# number of seconds that child waits for input from client
\$CTIMEOUT = 15;

# set to 1 to save the cookie value in a file (for scripting)
\$SAVE_COOKIE = 1;

\$INSTALLDIR = '%{_datadir}/autopsy/';

# System Utilities
\$STRINGS_EXE = '%{_bindir}/strings';
\$GREP_EXE = '/bin/grep';
\$FILE_EXE = '%{_bindir}/file';
\$MD5_EXE = '%{_bindir}/md5sum';
\$SHA1_EXE = '%{_bindir}/sha1sum';

# Directories
\$TSKDIR = '%{_bindir}/';
\$NSRLDB = '';
\$LOCKDIR = '%{_localstatedir}/lib/morgue';
EOF

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_mandir}/man1
install -d %{buildroot}/var/log/autopsy
install -d %{buildroot}%{_localstatedir}/lib/morgue
install -d %{buildroot}%{_datadir}/autopsy/help
install -d %{buildroot}%{_datadir}/autopsy/lib
install -d %{buildroot}%{_datadir}/autopsy/pict

install -m0755 autopsy %{buildroot}%{_sbindir}/autopsy
install -m0755 make-live-cd %{buildroot}%{_sbindir}/make-live-cd
install -m0755 conf.pl %{buildroot}%{_datadir}/autopsy/
install -m0644 help/*.html %{buildroot}%{_datadir}/autopsy/help/
install -m0644 lib/*.p* %{buildroot}%{_datadir}/autopsy/lib/
install -m0644 man/man1/autopsy.1 %{buildroot}%{_mandir}/man1/
install -m0644 pict/* %{buildroot}%{_datadir}/autopsy/pict/

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc CHANGES.txt COPYING docs/*.txt INSTALL.txt README-LIVE.txt README.txt TODO.txt
%config(noreplace) %attr(0644,root,root) %{_datadir}/autopsy/conf.pl
%config(noreplace) %attr(0644,root,root) %{_datadir}/autopsy/lib/define.pl
%{_datadir}/autopsy
%attr(0755,root,root) %{_sbindir}/autopsy
%attr(0755,root,root) %{_sbindir}/make-live-cd
%dir /var/log/autopsy
%dir %{_localstatedir}/lib/morgue
%attr(0644,root,root) %{_mandir}/man1/*
