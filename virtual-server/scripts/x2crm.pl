
# script_x2crm_desc()
sub script_x2crm_desc
{
return "X2Engine";
}

sub script_x2crm_uses
{
return ( "php" );
}

sub script_x2crm_longdesc
{
return "X2Engine is a fast and compact Marketing Automation, Sales Force and Customer Service application powered by an easy to use website-optimized visual workflow engine.";
}

# script_x2crm_versions()
sub script_x2crm_versions
{
return ( "4.3" );
}

sub script_x2crm_category
{
return "Commerce";
}

sub script_x2crm_php_vers
{
return ( 5 );
}

sub script_x2crm_php_modules
{
return ( "mysql", "imap" );
}

sub script_x2crm_dbs
{
return ( "mysql" );
}

# script_x2crm_depends(&domain, version)
sub script_x2crm_depends
{
local ($d, $ver, $sinfo, $phpver) = @_;
local @rv;

# Check for PHP 5.3+
local $phpv = &get_php_version($phpver || 5, $d);
if (!$phpv) {
	push(@rv, "Could not work out exact PHP version");
	}
elsif ($phpv < 5.2) {
	push(@rv, "X2Engine requires PHP version 5.3 or later");
	}

return @rv;
}

# script_x2crm_params(&domain, version, &upgrade-info)
# Returns HTML for table rows for options for installing X2Engine
sub script_x2crm_params
{
local ($d, $ver, $upgrade) = @_;
local $rv;
local $hdir = &public_html_dir($d, 1);
if ($upgrade) {
	# Options are fixed when upgrading
	local ($dbtype, $dbname) = split(/_/, $upgrade->{'opts'}->{'db'}, 2);
	$rv .= &ui_table_row("Database for X2Engine tables", $dbname);
	local $dir = $upgrade->{'opts'}->{'dir'};
	$dir =~ s/^$d->{'home'}\///;
	$rv .= &ui_table_row("Install directory", $dir);
	}
else {
	# Show editable install options
	local @dbs = &domain_databases($d, [ "mysql" ]);
	$rv .= &ui_table_row("Database for X2Engine tables",
		     &ui_database_select("db", undef, \@dbs, $d, "x2crm"));
	$rv .= &ui_table_row("Install sub-directory under <tt>$hdir</tt>",
			     &ui_opt_textbox("dir", &substitute_scriptname_template("x2crm", $d), 30, "At top level"));
	}
return $rv;
}

# script_x2crm_parse(&domain, version, &in, &upgrade-info)
# Returns either a hash ref of parsed options, or an error string
sub script_x2crm_parse
{
local ($d, $ver, $in, $upgrade) = @_;
if ($upgrade) {
	# Options are always the same
	return $upgrade->{'opts'};
	}
else {
	local $hdir = &public_html_dir($d, 0);
	$in{'dir_def'} || $in{'dir'} =~ /\S/ && $in{'dir'} !~ /\.\./ ||
		return "Missing or invalid installation directory";
	local $dir = $in{'dir_def'} ? $hdir : "$hdir/$in{'dir'}";
	local ($newdb) = ($in->{'db'} =~ s/^\*//);
	return { 'db' => $in->{'db'},
		 'newdb' => $newdb,
	         'dir' => $dir,
		 'path' => $in{'dir_def'} ? "/" : "/$in{'dir'}", };
	}
}

# script_x2crm_check(&domain, version, &opts, &upgrade-info)
# Returns an error message if a required option is missing or invalid
sub script_x2crm_check
{
local ($d, $ver, $opts, $upgrade) = @_;
$opts->{'dir'} =~ /^\// || return "Missing or invalid install directory";
$opts->{'db'} || return "Missing database";
if (-r "$opts->{'dir'}/initialize.php") {
	return "X2Engine appears to be already installed in the selected directory";
	}
local ($dbtype, $dbname) = split(/_/, $opts->{'db'}, 2);
local $clash = &find_database_table($dbtype, $dbname, "x2_");
$clash && return "X2Engine appears to be already using the selected database (table $clash)";
return undef;
}

# script_x2crm_files(&domain, version, &opts, &upgrade-info)
# Returns a list of files needed by X2Engine, each of which is a hash ref
# containing a name, filename and URL
sub script_x2crm_files
{
local ($d, $ver, $opts, $upgrade) = @_;
local @files = ( { 'name' => "source",
	   'file' => "X2Engine-$ver.zip",
	   'url' => "http://downloads.sourceforge.net/project/x2engine/X2Engine-$ver.zip" });
return @files;
}

sub script_x2crm_commands
{
return ("unzip");
}

# script_x2crm_install(&domain, version, &opts, &files, &upgrade-info)
# Actually installs X2Engine, and returns either 1 and an informational
# message, or 0 and an error
sub script_x2crm_install
{
local ($d, $version, $opts, $files, $upgrade, $domuser, $dompass) = @_;
local ($out, $ex);

if ($opts->{'newdb'} && !$upgrade) {
	local $err = &create_script_database($d, $opts->{'db'});
	return (0, "Database creation failed : $err") if ($err);
	}
local ($dbtype, $dbname) = split(/_/, $opts->{'db'}, 2);
local $dbuser = &mysql_user($d);
local $dbpass = &mysql_pass($d);
local $dbhost = &get_database_host($dbtype);
local $dberr = &check_script_db_connection($dbtype, $dbname, $dbuser, $dbpass);
return (0, "Database connection failed : $dberr") if ($dberr);

# Extract tar file to temp dir and copy to target
local $temp = &transname();
local $err = &extract_script_archive($files->{'source'}, $temp, $d,
                                     $opts->{'dir'}, "X2Engine-*/x2engine");
$err && return (0, "Failed to extract source : $err");

# Update the install config file
local $url = &script_path_url($d, $opts);
local $cfile = "$opts->{'dir'}/installConfig.php";
local $lref = &read_file_lines_as_domain_user($d, $cfile);
foreach my $l (@$lref) {
	if ($l =~ /^\$host\s*=/) {
		$l = "\$host = '$dbhost';";
		}
	if ($l =~ /^\$db\s*=/) {
		$l = "\$db = '$dbname';";
		}
	if ($l =~ /^\$user\s*=/) {
		$l = "\$user = '$dbuser';";
		}
	if ($l =~ /^\$pass\s*=/) {
		$l = "\$pass = '$dbpass';";
		}
	if ($l =~ /^\$adminEmail\s*=/) {
		$l = "\$adminEmail = '$d->{'emailto_addr'}';";
		}
	if ($l =~ /^\$adminUsername\s*=/) {
		$l = "\$adminUsername = '$domuser';";
		}
	if ($l =~ /^\$adminPassword\s*=/) {
		$l = "\$adminPassword = '$dompass';";
		}
	}
&flush_file_lines_as_domain_user($d, $cfile);

# Build the command line to call X2Engine's install script
local ($p5) = grep { $_->[0] == $opts->{'phpver'} }
		   &list_available_php_versions($d);
local $cmd = $p5->[1];
if (!$cmd) {
	$cmd = &has_command("php5") ||
	       &has_command("php");
	}
$cmd =~ s/-cgi$//;
$cmd .= " initialize.php silent";
local $phpver = $opts->{'phpver'} || 5;
if (-d "$d->{'home'}/etc/php$phpver") {
	$cmd = "PHPRC=$d->{'home'}/etc/php$phpver $cmd";
	}

# Run it as the domain owner
local $out = &run_as_domain_user($d,
	"cd ".quotemeta($opts->{'dir'})." && ".$cmd." 2>&1");
if ($? || $out =~ /FAILED/) {
	return (-1, "Installation script failed : <pre>".
		    &html_escape($out)."</pre>");
	}

# Tell the user about the new install
local $rp = $opts->{'dir'};
$rp =~ s/^$d->{'home'}\///;
return (1, "Initial X2Engine installation complete. Go to <a target=_blank href='$url'>$url</a> to manage it.", "Under $rp using MySQL database $dbname", $url, $domuser, $dompass );
}

# script_x2crm_uninstall(&domain, version, &opts)
# Un-installs a X2Engine installation, by removing it's files
# Returns 1 on success and a message, or 0 on failure and an error
sub script_x2crm_uninstall
{
local ($d, $version, $opts) = @_;

# Remove x2crm tables from the database
&cleanup_script_database($d, $opts->{'db'}, "x2_");

# Remove the contents of the target directory
local $derr = &delete_script_install_directory($d, $opts);
return (0, $derr) if ($derr);

# Take out the DB
if ($opts->{'newdb'}) {
	&delete_script_database($d, $opts->{'db'});
	}

return (1, "Deleted X2Engine directory and tables.");
}

# script_x2crm_check_latest(version)
# Checks if some version is the latest for this project, and if not returns
# a newer one. Otherwise returns undef.
sub script_x2crm_check_latest
{
local ($ver) = @_;
local @vers = &osdn_package_versions(
	"x2engine", "X2Engine-([0-9\\.]+).zip");
return "Failed to find versions" if (!@vers);
return $ver eq $vers[0] ? undef : $vers[0];
}

sub script_x2crm_site
{
return 'http://www.x2engine.com/';
}

sub script_x2crm_passmode
{
return 1;
}

1;

