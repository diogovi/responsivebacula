#!/usr/bin/perl
# Show the Bacula main menu

require './bacula-backup-lib.pl';
$hsl = &help_search_link( "bacula", "man", "doc", "google" );

# Make sure it is installed
$err = &check_bacula();
if ($err) {
	&ui_print_header( undef, $module_info{'desc'}, "", "intro", 1, 1, 0, $hsl );
	print &ui_config_link( 'index_echeck', [ $err, undef ] ), "<p>\n";
	&ui_print_footer( "/", $text{'index'} );
	exit;
}

if ( &has_bacula_dir() ) {

	# Test DB connection
	eval { $dbh = &connect_to_database(); };
	if ($@) {
		$err = $@;
		&ui_print_header( undef, $module_info{'desc'}, "", "intro", 1, 1, 0,
			$hsl );
		print &ui_config_link( 'index_edb', [ $err, undef ] ), "<p>\n";
		&ui_print_footer( "/", $text{'index'} );
		exit;
	}
	$dbh->disconnect();
}

# Test node group DB
if ( &has_bacula_dir() && &has_node_groups() ) {
	$err = &check_node_groups();
	if ($err) {
		&ui_print_header( undef, $module_info{'desc'}, "", "intro", 1, 1, 0,
			$hsl );
		print &ui_config_link( 'index_eng', [ $err, undef ] ), "<p>\n";
		&ui_print_footer( "/", $text{'index'} );
		exit;
	}
}

# Get the Bacula version, and check it
$ver = &get_bacula_version();

&ui_print_header( undef, $module_info{'desc'}, "", "intro", 1, 1, 0, $hsl,
	undef, undef, undef );

# ($ver ? &text('index_version'.$cmd_prefix, $ver)."<br>" : undef));
if ( $ver && $ver < 1.36 ) {
	print &text( 'index_eversion', 1.36, $ver ), "<p>\n";
	&ui_print_footer( "/", $text{'index'} );
	exit;
}

# Make sure bconsole works
if ( &is_bacula_running( $cmd_prefix . "-dir" ) ) {

	# Check hostname in console config
	$conconf = &get_bconsole_config();
	$condir  = &find( "Director", $conconf );
	$conaddr = &find_value( "Address", $condir->{'members'} );
	if ( !&to_ipaddress($conaddr) && !&to_ip6address($conaddr) ) {

		# Offer to fix hostname
		print &text( 'index_econsole2', "<tt>$console_cmd</tt>",
			"<tt>$conaddr</tt>" ),
		  "<p>\n";
		print &ui_form_start("fixaddr.cgi");
		print &ui_form_end( [ [ "fix", $text{'index_fixaddr'} ] ] );
		&ui_print_footer( "/", $text{'index'} );
		exit;
	}

	# Test run bconsole
	local $status;
	eval {
		local $h = &open_console();
		$status = &console_cmd( $h, "version" );
		&close_console($h);
	};
	if ( $status !~ /Version/i ) {

		# Nope .. check if there is a password mismatch we can fix
		print &text(
			'index_econsole',
			"<tt>$console_cmd</tt>",
			"<tt>$config{'bacula_dir'}/bconsole.conf</tt>"
		  ),
		  "<p>\n";
		$dirconf = &get_director_config();
		$dirdir  = &find( "Director", $dirconf );
		$dirpass = &find_value( "Password", $dirdir->{'members'} );
		$conpass = &find_value( "Password", $condir->{'members'} );
		if ( $dirpass && $conpass && $dirpass ne $conpass ) {

			# Can fix!
			print &ui_form_start("fixpass.cgi");
			print &ui_form_end( [ [ "fix", $text{'index_fixpass'} ] ] );
		}
		&ui_print_footer( "/", $text{'index'} );
		exit;
	}
}

# sections

$sec = 0;

sub section_open {
	$sec = $sec + 1;
	if ( $sec % 2 ) {
		$sect = "color_b";
	}
	else {
		$sect = "color_a";
	}
	#$sec % 2 ? $sect = "color_b" : $sect = "color_a";

	print '<section class="' . $sect . '">';
}

sub section_close {
	print '</section>';
}

# Show director, storage and file daemon icons
if ( &has_bacula_dir() ) {

	&section_open;
	print &ui_subheading( $text{'index_dir'} );

	#print &theme_ui_subheading($text{'index_dir'});
	@pages = (
		"director", "clients", "filesets", "schedules",
		"jobs",     "pools",   "storages"
	);
	&show_icons_from_pages( \@pages );
	&section_close;
}
if ( &has_bacula_sd() ) {
	&section_open;
	print &ui_subheading( $text{'index_sd'} );
	@pages = ( "storagec", "devices" );
	if ( !&has_bacula_dir() || $config{'showdirs'} ) {

		push( @pages, "sdirectors" );
	}
	&show_icons_from_pages( \@pages );
	&section_close;
}
if ( &has_bacula_fd() ) {
	&section_open;
	print &ui_subheading( $text{'index_fd'} );
	@pages = ("file");
	if ( !&has_bacula_dir() || $config{'showdirs'} ) {
		push( @pages, "fdirectors" );
	}
	&show_icons_from_pages( \@pages );
	&section_close;
}

# Show icons for node group operations
if ( &has_bacula_dir() && &has_node_groups() ) {
	&section_open;
	print &ui_subheading( $text{'index_groups'} );
	@pages = ( "groups", "gjobs", "gbackup", "sync" );
	@links  = map { "list_${_}.cgi" } @pages;
	@titles = map { $text{"${_}_title"} } @pages;
	@icons  = map { "images/${_}.gif" } @pages;

	#&icons_table(\@links, \@titles, \@icons);
	&show_icons_from_pages( \@pages );
	&section_close;
}

if ( &has_bacula_dir() ) {
	&section_open;

	# Show icons for actions
	print &ui_hr();
	print &ui_subheading( $text{'index_actions'} );
	if ( &is_bacula_running( $cmd_prefix . "-dir" ) ) {
		@actions = (
			"backup", "dirstatus",  "clientstatus", "storagestatus",
			"label",  "poolstatus", "mount",        "restore"
		);

		@links  = map { "${_}_form.cgi" } @actions;
		@titles = map { $text{"${_}_title"} } @actions;
		@icons  = map { "images/${_}.gif" } @actions;
		&show_icons_from_actions( \@actions );

	}
	else {
		print "<b>$text{'index_notrun'}</b><p>\n";
	}
	&section_close;
}
my %access = &get_module_acl();
if ( !$access{'noconfig'} && !$config{'noprefs'} ) {
	&section_open;
	print &ui_hr();
	#print &ui_subheading( $text{'index_actions'} );
	print &ui_subheading( "YO" );
	my $cprog = $user_module_config_directory ? "uconfig.cgi" : "config.cgi";
	print "<a href=\"$gconfig{'webprefix'}/$cprog?",
	  	&get_module_name() . "\">",
		"<div class=\"large-3 medium-6 small-12 columns text-center padding_b_2rem\">\n",
		  "<i class=\"fa fa-main fa-cog\"></i>\n",
		  "<div class=\"large-12 columns text-center fa-label\">Admin</div>\n",
		  "</div></a>\n";

	&section_close;
}


sub show_icons_from_actions {
	local ($pages) = @_;
	local @links  = map { "${_}_form.cgi" } @$pages;
	local @titles = map { $text{"${_}_title"} } @$pages;
	local @iconx  = map { &map_icon($_) } @$pages;
	&icons_table_( \@links, \@titles, \@iconx );

}
print &ui_hr();

# See what processes are running
print "<b>$text{'index_status'}</b>\n";
foreach $p (@bacula_processes) {
	print "&nbsp;|&nbsp;\n" if ( $p ne $bacula_processes[0] );
	print $text{ 'proc_' . $p }, " - ";
	if ( &is_bacula_running($p) ) {
		print "<font color=#00aa00><b>", $text{'index_up'}, "</b></font>\n";
		$pcount++;
	}
	else {
		print "<font color=#ff0000><b>", $text{'index_down'}, "</b></font>\n";
	}
}
print "<p>\n";
print &ui_buttons_start();
if ( $pcount > 0 ) {
	if ( !$config{'apply'} ) {
		print &ui_buttons_row( "apply.cgi", $text{'index_apply'},
			$text{'index_applydesc'} );
	}
	if ( &has_bacula_dir() ) {

		# Only show restart button if we are running the director, as
		# for others the apply does a restart
		print &ui_buttons_row( "restart.cgi", $text{'index_restart'},
			$text{'index_restartdesc'} );
	}
	print &ui_buttons_row( "stop.cgi", $text{'index_stop'},
		$text{'index_stopdesc'} );
}
if ( $pcount < scalar(@bacula_processes) ) {
	print &ui_buttons_row( "start.cgi", $text{'index_start'},
		$text{'index_startdesc'} );
}

# See what is started at boot
if ( &foreign_installed("init") ) {
	&foreign_require( "init", "init-lib.pl" );
	$status = &init::action_status( $bacula_inits[0] );
	if ($status) {
		print &ui_buttons_row( "bootup.cgi", $text{'index_boot'},
			$text{'index_bootdesc'}, undef,
			&ui_yesno_radio( "boot", $status == 2 ? 1 : 0 ) );
	}
}

print &ui_buttons_end();

&ui_print_footer( "/", $text{'index'} );

sub map_icon {
	local ($category) = @_;
	use feature qw(switch);
	given ($category) {
		when ('director') { $icon = 'fa-cog'; }

		#when('Director Configuration') { $icon = 'fa-cog'; }
		when ('clients')   { $icon = 'fa-users'; }
		when ('filesets')  { $icon = 'fa-file'; }
		when ('servers')   { $icon = 'fa-rocket'; }
		when ('schedules') { $icon = 'fa-clock-o'; }
		when ('jobs')      { $icon = 'fa-calendar'; }
		when ('pools')     { $icon = 'fa-cubes'; }
		when ('storages')  { $icon = 'fa-hdd-o'; }

		when ('storagec') { $icon = 'fa-cog'; }
		when ('devices')  { $icon = 'fa-archive'; }

		when ('backup')        { $icon = 'fa-hdd-o'; }
		when ('dirstatus')     { $icon = 'fa-user'; }
		when ('clientstatus')  { $icon = 'fa-info-circle'; }
		when ('storagestatus') { $icon = 'fa-archive'; }
		when ('label')         { $icon = 'fa-cube'; }
		when ('poolstatus')    { $icon = 'fa-cubes'; }
		when ('mount')         { $icon = 'fa-exchange'; }
		when ('restore')       { $icon = 'fa-history'; }

		default { $icon = 'fa-rocket'; };
	}
	return $icon;
}

sub show_icons_from_pages {
	local ($pages) = @_;
	local @links = map {
		$_ eq "director" || $_ eq "file" || $_ eq "storagec"
		  ? "edit_${_}.cgi"
		  : "list_${_}.cgi"
	} @$pages;
	local @titles = map { $text{"${_}_title"} } @$pages;
	local @iconx = map { &map_icon($_) } @$pages;
	&icons_table_( \@links, \@titles, \@iconx );
}

sub logg {
	open my $fh, ">", '/var/log/perl.log'
	  or die "Can't open the fscking file: $!";
	$text = $_[0] . "\n";
	print $fh $text;
}

sub icons_table_ {
	local $icon=$_[2];
	local $label=$_[1];
	local $link=$_[0];
	print "<div class=\"row\">\n";
	for ( my $i = 0 ; $i < @{ $_[0] } ; $i++ ) {
		&generate_icon_( $icon->[$i], $label->[$i], $link->[$i],
			ref( $_[4] ) ? $_[4]->[$i] : $_[4],
			$_[5], $_[6], $_[7]->[$i], $_[8]->[$i] );
		&logg($link->[$i]);
	}
	print "</div>";
}

sub generate_icon_ {
		print "<a href=\"$_[2]\" $_[3]>\n",
		"<div class=\"large-3 medium-6 small-12 columns text-center padding_b_2rem\">\n",
		"<i class=\"fa fa-main $_[0]\"></i>\n",
		"<div class=\"large-12 columns text-center fa-label\">$_[1]</div>\n",
		"</div></a>\n";

}
