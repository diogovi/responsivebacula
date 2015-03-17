#!/usr/bin/perl
# Show the Bacula main menu

require './bacula-backup-lib.pl';
#require '../web-lib-funcs.pl';
$hsl = &help_search_link( "bacula", "man", "doc", "google" );
#%text = &load_language($current_theme);
# Make sure it is installed

$err = &check_bacula();
if ($err) {
	&ui_print_header( undef, $module_info{'desc'}, "", "intro", 1, 1, 0, $hsl );
	print &ui_config_link( 'index_echeck', [ $err, undef ] ), "<p>\n";
	&ui_print_footer( "/", ${'index'} );
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

#########################

&neos_header();

#########################


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
	#print &ui_hr();
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


#print &ui_hr();


#print "<p>\n";
#print &ui_buttons_start();
#&buttons();
&init_check();
#print &ui_buttons_end();
&ui_print_footer( "/", $text{'index'} );
&_end();

##########################################################################
sub admin
{
	my %access = &get_module_acl();
	if ( !$access{'noconfig'} && !$config{'noprefs'} ) {
		&section_open;
		#print &ui_hr();
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
}
sub running_procs
{
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
	return $pcount;
}

sub buttons 
{
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
}
sub buttons_neos
{
	if ( $pcount > 0 ) {
		if ( !$config{'apply'} ) {
			#print &neos_ui_buttons_row( "apply.cgi", $text{'index_apply'},
			#	$text{'index_applydesc'} );
			
		}
		if ( &has_bacula_dir() ) {
	
			# Only show restart button if we are running the director, as
			# for others the apply does a restart
			#print &neos_ui_buttons_row( "restart.cgi", $text{'index_restart'},
			#	$text{'index_restartdesc'} );
			print '<form action="restart.cgi">',
				'<div class="large-4 medium-4 small-4 left">',
				'<button type="submit" class="button restart_bacula" value="Restart Bacula">Restart Bacula</button></div>',
			#	'<div class="button restart_bacula">Click this button to shut down the Bacula daemon processes listed above.</div> ',
				'</form>';
		}
		#print &neos_ui_buttons_row( "stop.cgi", $text{'index_stop'},
		#		$text{'index_stopdesc'} );
		print '<form action="stop.cgi">',
			'<div class="large-4 medium-4 small-4 left">',
			'<button type="submit" class="button restart_bacula" value="Stop Bacula">Stop Bacula</button></div> ',
		#	'<div class="button stop_bacula">Click this button to shut down the Bacula daemon processes listed above.</div> ',
			'</form>';		
	}
	if ( $pcount < scalar(@bacula_processes) ) {
		#print &neos_ui_buttons_row( "start.cgi", $text{'index_start'},
		#	$text{'index_startdesc'} );
		print '<form action="start.cgi">',
			'<div class="large-4 medium-4 small-4 left">', 
			'<button type="submit" class="button restart_bacula" value="Start Bacula">Start Bacula</button></div> ',
		#	'<div class="button stop_bacula">Click this button to shut down the Bacula daemon processes listed above.</div> ',
			'</form>';	
	}
}

sub init_check
{
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
}

sub show_icons_from_actions {
	local ($pages) = @_;
	local @links  = map { "${_}_form.cgi" } @$pages;
	local @titles = map { $text{"${_}_title"} } @$pages;
	local @iconx  = map { &map_icon($_) } @$pages;
	&icons_table_( \@links, \@titles, \@iconx );

}

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
		#&logg($link->[$i]);
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

sub ui_print_header_
{
	my ($text, @args) = @_;
	&header_(@args);
	#print &ui_post_header($text);
}
sub header_
{
	return if ($main::done_webmin_header++);
	my $ll;
	my $charset = defined($main::force_charset) ? $main::force_charset
						    : &get_charset();
	&PrintHeader($charset);
	&load_theme_library();
	if (defined(&theme_header)) {
		$module_name = &get_module_name();
		&theme_header(@_);
		$miniserv::page_capture = 1;
		return;
		}
	print "<!doctype html public \"-//W3C//DTD HTML 3.2 Final//EN\">\n";
	print "<html>\n";
	print "<head>\n";
	if (defined(&theme_prehead)) {
		&theme_prehead(@_);
		}
	if ($charset) {
		print "<meta http-equiv=\"Content-Type\" ",
		      "content=\"text/html; Charset=".&quote_escape($charset)."\">\n";
		}
	if (@_ > 0) {
		my $title = &get_html_title($_[0]);
	        print "<title>$title</title>\n" if ($_[7] !~ /<title>/i);
		print $_[7] if ($_[7]);
		print &get_html_status_line(0);
		}
	print "$tconfig{'headhtml'}\n" if ($tconfig{'headhtml'});
	if ($tconfig{'headinclude'}) {
		print &read_file_contents(
			"$theme_root_directory/$tconfig{'headinclude'}");
		}
	print "</head>\n";
	my $bgcolor = defined($tconfig{'cs_page'}) ? $tconfig{'cs_page'} :
			 defined($gconfig{'cs_page'}) ? $gconfig{'cs_page'} : "ffffff";
	my $link = defined($tconfig{'cs_link'}) ? $tconfig{'cs_link'} :
		      defined($gconfig{'cs_link'}) ? $gconfig{'cs_link'} : "0000ee";
	my $text = defined($tconfig{'cs_text'}) ? $tconfig{'cs_text'} : 
		      defined($gconfig{'cs_text'}) ? $gconfig{'cs_text'} : "000000";
	my $bgimage = defined($tconfig{'bgimage'}) ? "background=$tconfig{'bgimage'}" : "";
	my $dir = $current_lang_info->{'dir'} ? "dir=\"$current_lang_info->{'dir'}\"" : "";
	my $html_body = "<body bgcolor=#$bgcolor link=#$link vlink=#$link text=#$text $bgimage $tconfig{'inbody'} $dir $_[8]>\n";
	$html_body =~ s/\s+\>/>/g;
	print $html_body;
	
	if (defined(&theme_prebody)) {
		&theme_prebody(@_);
		}
	my $hostname = &get_display_hostname();
	my $version = &get_webmin_version();
	my $prebody = $tconfig{'prebody'};
	if ($prebody) {
		$prebody =~ s/%HOSTNAME%/$hostname/g;
		$prebody =~ s/%VERSION%/$version/g;
		$prebody =~ s/%USER%/$remote_user/g;
		$prebody =~ s/%OS%/$os_type $os_version/g;
		print "$prebody\n";
		}
	if ($tconfig{'prebodyinclude'}) {
		local $_;
		open(INC, "$theme_root_directory/$tconfig{'prebodyinclude'}");
		while(<INC>) {
			print;
			}
		close(INC);
		}
	if (@_ > 1) {
		print $tconfig{'preheader'};
		my %this_module_info = &get_module_info(&get_module_name());
		print "<table class='header' width=100%><tr>\n";
		if ($gconfig{'sysinfo'} == 2 && $remote_user) {
			print "<td id='headln1' colspan=3 align=center>\n";
			print &get_html_status_line(1);
			print "</td></tr> <tr>\n";
			}
		print "<td id='headln2l' width=15% valign=top align=left>";
		if ($ENV{'HTTP_WEBMIN_SERVERS'} && !$tconfig{'framed'}) {
			print "<a href='$ENV{'HTTP_WEBMIN_SERVERS'}'>",
			      "$text{'header_servers'}</a><br>\n";
			}
		if (!$_[5] && !$tconfig{'noindex'}) {
			my @avail = &get_available_module_infos(1);
			my $nolo = $ENV{'ANONYMOUS_USER'} ||
				      $ENV{'SSL_USER'} || $ENV{'LOCAL_USER'} ||
				      $ENV{'HTTP_USER_AGENT'} =~ /webmin/i;
			if ($gconfig{'gotoone'} && $main::session_id && @avail == 1 &&
			    !$nolo) {
				print "<a href='$gconfig{'webprefix'}/session_login.cgi?logout=1'>",
				      "$text{'main_logout'}</a><br>";
				}
			elsif ($gconfig{'gotoone'} && @avail == 1 && !$nolo) {
				print "<a href=$gconfig{'webprefix'}/switch_user.cgi>",
				      "$text{'main_switch'}</a><br>";
				}
			elsif (!$gconfig{'gotoone'} || @avail > 1) {
				print "<a href='$gconfig{'webprefix'}/?cat=",
				      $this_module_info{'category'},
				      "'>$text{'header_webmin'}</a><br>\n";
				}
			}
		if (!$_[4] && !$tconfig{'nomoduleindex'}) {
			my $idx = $this_module_info{'index_link'};
			my $mi = $module_index_link || "/".&get_module_name()."/$idx";
			my $mt = $module_index_name || $text{'header_module'};
			print "<a href=\"$gconfig{'webprefix'}$mi\">$mt</a><br>\n";
			}
		if (ref($_[2]) eq "ARRAY" && !$ENV{'ANONYMOUS_USER'} &&
		    !$tconfig{'nohelp'}) {
			print &hlink($text{'header_help'}, $_[2]->[0], $_[2]->[1]),
			      "<br>\n";
			}
		elsif (defined($_[2]) && !$ENV{'ANONYMOUS_USER'} &&
		       !$tconfig{'nohelp'}) {
			print &hlink($text{'header_help'}, $_[2]),"<br>\n";
			}
		if ($_[3]) {
			my %access = &get_module_acl();
			if (!$access{'noconfig'} && !$config{'noprefs'}) {
				my $cprog = $user_module_config_directory ?
						"uconfig.cgi" : "config.cgi";
				print "<a href=\"$gconfig{'webprefix'}/$cprog?",
				      &get_module_name()."\">",
				      $text{'header_config'},"</a><br>\n";
				}
			}
		print "</td>\n";
		if ($_[1]) {
			# Title is a single image
			print "<td id='headln2c' align=center width=70%>",
			      "<img alt=\"$_[0]\" src=\"$_[1]\"></td>\n";
			}
		else {
			# Title is just text
			my $ts = defined($tconfig{'titlesize'}) ?
					$tconfig{'titlesize'} : "+2";
			print "<td id='headln2c' align=center width=70%>",
			      ($ts ? "<font size=$ts>" : ""),$_[0],
			      ($ts ? "</font>" : "");
			print "<br>$_[9]\n" if ($_[9]);
			print "</td>\n";
			}
		print "<td id='headln2r' width=15% valign=top align=right>";
		print $_[6];
		print "</td></tr></table>\n";
		print $tconfig{'postheader'};
		}
	$miniserv::page_capture = 1;
}

sub neos_header 
{
	print '<!-- Top bar/Nav e Side bar -->' , "\n";
	print '<div class="off-canvas-wrap fixed" data-offcanvas>' , "\n";
	print '<div class="inner-wrap">' , "\n";
	print '<nav class="top-bar tab-bar">' , "\n";
	
	print '<!-- Title -->' , "\n";
	print '<div class="large-4 medium-4 small-4 columns ">' , "\n";
	print '<ul class="title-area">' , "\n";
	print '<li class="name row">' , "\n";
	#print '<h1><a href="/"><span class="bacula-title">Webmin ' . &get_webmin_version() . '</span></a></h1>' , "\n";
	print '<h1><a href="/"><span class="bacula-title">Bacula</span><span class="backups-title"> Backups</span></a></h1>' , "\n";
	#    print '<small><i class="fa fa-user">&nbsp;</i></small>&nbsp;'
	#        . ucfirst( &get_product_name() )
	#        . '<span class="hidden-xs">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<small><i class="fa fa-desktop">&nbsp;</i></small></span>&nbsp;&nbsp;<a class="data-refresh hidden-xs" href="/" style="color:#777">'
	#        . &get_display_hostname() . '</a>';
	print '</li>' , "\n";
	print '</ul>' , "\n";
	print '</div>' , "\n";
	print '<!-- Logo -->' , "\n";
	
	print '<div class="large-4 columns hide-for-medium hide-for-small central-logo">' , "\n";
	print '<img class="bacula_logo" src="/unauthenticated/img/logos/bacula_logo.png" alt="Bacula Backups">' , "\n";
	print '</div>' , "\n";
	
	print '<!-- Top Bar Right Nav Elements + Search -->' , "\n";
	print '<div class="large-3 hide-for-small right search">' , "\n";
	
	print '<div class="has-form">' , "\n";
	if (-r "$root_directory/webmin_search.cgi" && $gaccess{'webminsearch'}) {
		&print_menu_search();
	}
	print '<div class="row collapse">' , "\n";
	
	print '<div class="large-10 medium-10  columns">' , "\n";
	#print '<input type="text" placeholder="Find">' , "\n";
	print '</div>' , "\n";
	print '<div class="large-2 medium-2  columns">' , "\n";
	#print '<a href="#" class="search button expand"><i class="fa fa-search fa-2x"></i></a>' , "\n";
	
	print '</div>' , "\n";
	print '</div>' , "\n";
	print '</div>' , "\n";
	print '</div>' , "\n";
	
	print '<section class="right-small sidebar">' , "\n";
	print '<a class="right-off-canvas-toggle" href="#"><i class="fa fa-reorder fa-2x sidebutton"></i></a>' , "\n";
	print '</section>' , "\n";
	print '</nav>' , "\n";
	
	print '<aside class="right-off-canvas-menu">' , "\n";
		print '<ul class="off-canvas-list">' , "\n";
		#print '<!--list header-->' , "\n";
		print '<!--list header-->' , "\n";
		print '<li><label><i class="fa fa-refresh fa-1x center refresh right"></i></label></li>' , "\n";
		print '<!--search-->' , "\n";
		#print '<!--search-->' , "\n";
		print '<li class="show-for-small-only find">' , "\n"; 
		print '<a href="#" class="width25"><i class="fa fa-search fa-1x small-6"></i></a>' , "\n";
		print '<input type="text" class="small-6 width75" placeholder="Find">' , "\n";
		print '</li>' , "\n";	
		#print '<!--list body-->' , "\n";
		print '<!--list body-->' , "\n";
		#@cats = &get_visible_modules_categories();
		#@cats = ("System_hostname","Operating_system","Webmin_version","CPU_load_averages","Real_memory","Virtual_memory","Local_disk_space");
		# chamar o modulo system-status
		&foreign_require("system-status");
		$info = &system_status::get_collected_info();
		# Operating System Info
		if ($gconfig{'os_version'} eq '*') {
			$os = $gconfig{'real_os_type'};
		} else {
			$os = $gconfig{'real_os_type'} . ' ' . $gconfig{'real_os_version'};
		}
		# Load averages
		if ($info->{'load'}) {
			@c = @{$info->{'load'}};
			if (@c) {
				#&print_table_row($text{'body_cpu'}, &text('body_load', @c));
				#@a = ("cenas",&text('body_load', @c));
				#local ($tit, $cont) = @a;
				#%text2 = &load_language($current_theme);
				#$load = &text('body_load', @c);
				#$load= (join("+",@c));
				#&logg("c=" . (join("+",@c)));
				#&logg("text=" . (join("+",@text)));
				#&logg("1 min=".$c[0]);
				#&logg("5 mins=".$c[1]);
				#&logg("15 mins=".$c[2]);
				$load = $c[0] . " (1 min) " . $c[1] . " (5 mins) " . $c[2] . " (15 mins)";
				#foreach (sort keys %text) {
				#	$cenas.= "$_ : $myhash{$_}\n";	
				#}
			#	&logg($cenas);
				#&logg("text1=" . $text{'body_cpu'});
				
				#&logg("text2=" . &text('body_load', @c));
				#&logg("text3=" . &text('body_load'));
				#&logg("load=" . $load);
				
				#$t = &get_module_variable('%text2', 1);
				#$rv = exists($t->{'body_load'}) ? $t->{'body_load'} : $text{'body_load'};
				#$rv =~ s/\$(\d+)/$1 < @_ ? $_[$1] : '$'.$1/ge;
				#&logg("load=" . $rv);
				
			}
		}
		# CPU Usage
		$cpu=0;
		if ($info->{'cpu'}) {
			@c = @{$info->{'cpu'}};
			$cpu = $c[0]+$c[1]+$c[3];
			#&print_progressbar_colum(6, $col_width, $used, 'CPU');
		}
		# MEM e VIRT Usage
		$mem=0;
		$virt=0;
		if ($info->{'mem'}) {
			@m = @{$info->{'mem'}};
			if (@m && $m[0]) {
				$mem = sprintf("%.0f",($m[0]-$m[1])/$m[0]*100);
				#&print_progressbar_colum(6, $col_width, $used, 'MEM');
			}
			if (@m && $m[2]) {
				$virt = sprintf("%.0f",($m[2]-$m[3])/$m[2]*100);
				#&print_progressbar_colum(6, $col_width, $used, 'VIRT');
			}
		}
		# HDD Usage
		$hdd=0;
		if ($info->{'disk_total'}) {
			($total, $free) = ($info->{'disk_total'}, $info->{'disk_free'});
			$hdd = sprintf("%.0f",($total-$free)/$total*100);
			#&print_progressbar_colum(6, $col_width, $used, 'HDD');
		}
		%cats = (
			'System_hostname' => [{'order' => '0', 'name' => 'System hostname', 'value' => &get_display_hostname()},],
			'Operating_system' => [{'order' => '1', 'name' => 'Operating system', 'value' => $os },],
			'Webmin_version' => [{'order' => '2', 'name' => 'Webmin version', 'value' => &get_webmin_version()},],
			'CPU_load_averages' => [{'order' => '3', 'name' => 'CPU load averages', 'value' => $load},],
			'Real_memory' => [{'order' => '4', 'name' => 'Real memory', 'value' => $mem . "%"},],
			'Virtual_memory' => [{'order' => '5', 'name' => 'Virtual memory', 'value' => $virt . "%"},],
			'Local_disk_space' => [{'order' => '6', 'name' => 'Local disk space', 'value' => $hdd . "%"},],
			);

		#@modules = map { @{$_->{'modules'}} } @cats;
		#@modules = ("System hostname","Operating system","Webmin version","CPU load averages","Real memory","Virtual memory","Local disk space");
		
		foreach $catt ( keys %cats) {
			foreach $cat ( @{ $cats{$catt} }) {
				#&print_menu_category($cat->{'code'}, $cat->{'desc'});
				print '<li>' . "\n";
					print '<a href="#" data-open="#' . $cat . '">' . "\n";
						#print '<i class="fa fa-fw fa-cog"></i>';
						print '<span class="aside-text">' . $cat->{'name'} . '<span class="aside-arrow" ><i class="fa fa-angle-right"></i></span></span>' . "\n";
					print '</a>' . "\n";
				print '</li>' . "\n";
				#&print_sub_category_opener($cat->{'code'});
				print '<li class="submenu" id="' . $cat . '">' . "\n";
					print '<ul class="aside-nav">' . "\n";
						#foreach $module (@{$cat->{'modules'}}) {
							#&print_sub_category($module->{'dir'} . '/', $module->{'desc'}, 'page-container');
							print '<li>' . "\n";
							$link="#";
							print '<a href="' . $link .'" target="_self">' . $cat->{'value'} . '</a>' . "\n";
							#print $cat->{'value'} . "\n";
							#print 'ok'. "\n";;
							print '</li>' . "\n";
						#}
						#&print_sub_category_closer();
					print '</ul>' . "\n";
				print '</li>' . "\n";
			}
		}
		if (-r "$root_directory/webmin_search.cgi" && $gaccess{'webminsearch'}) {
			&print_menu_search_right_off();
		}
	
		#print '<li><a href="#">System hostname</a></li>' , "\n";
		#print '<li><a href="#">Operating system</a></li>' , "\n";
		#print '<li><a href="#">Webmin version</a></li>' , "\n";
		#print '<li><a href="#">CPU load averages</a></li>' , "\n";
		#print '<li><a href="#">Real memory</a></li>' , "\n";
		#print '<li><a href="#">Virtual memory</a></li>' , "\n";
		#print '<li><a href="#">Local disk space</a></li>' , "\n";
		print '<li class="service_stats_button"><a href="#extreme"><span class="service"> Service Stats</span> <span class="fa fa-arrow-down fa-1x service right"></span></a></li>' , "\n";
		print '</ul>' . "\n";
		
		print '<!-- Buttons -->' . "\n";
      	print '<!-- Triggers the modals -->' . "\n";
      	$pcount = 0;
		&running_procs();
      	print '<div id="extreme" class="large-12 medium-12 small-12 restart_block">' . "\n";
      	
	      	&buttons_neos();
	      	#print '<div class="large-4 medium-4 small-4 left"><a href="#" data-reveal-id="restart_service" class="button restart_bacula">Restart Bacula</a></div>' . "\n"; 
	      	#print '<div class="large-4 medium-4 small-4 left"><a href="#" data-reveal-id="stop_service" class="button restart_bacula">Stop Bacula</a></div>' . "\n";
	      	
	      	#print '<div class="large-4 medium-4 small-4 left"><a href="#" data-reveal-id="start_service" class="button restart_bacula">Start at Boot</a></div>' . "\n";
	      #	print 'div class="large-12 medium-12 small-12 show-for-small-only left vi_logo_side">' . "\n";
	      #		print '<a href="http://www.versaointegral.pt"><img class="vi_logo"  src="img/logos/vi_logo.png" alt="Versão Integral"/></a>' . "\n";
	    #	print '</div>' . "\n";
      	#print '</div>' . "\n";

		print '<!-- Reveal Modals begin RESTART -->' , "\n";
		print '<div id="restart_service" class="reveal-modal" data-reveal>' , "\n";
			print '<h2>Wow! That\'s a little drastic...</h2>' , "\n";
			print '<p>Restarting the service requires a brief unavailability of the system.</br>' , "\n";
			print 'Confirming rhat you want to restart the service will stop and then start the system.</p>' , "\n";
			print '<p><a href="#" data-reveal-id="restart_service_B" class="secondary button">Confirm</a></p>' , "\n";
			print '<a class="close-reveal-modal right">&#215;</a>' , "\n";
		print '</div>' , "\n";
		print '<div id="restart_service_B" class="reveal-modal" data-reveal>' , "\n";
			print '<h2>Here we go! You\'ve set the service to Restart!</h2>' , "\n";
			print '<p>Your system will be restarted! Good luck :)</p>' , "\n";
			print '<a class="close-reveal-modal">&#215;</a>' , "\n";
			print '<!-- Reveal Modals begin STOP -->' , "\n";
			print '<div id="stop_service" class="reveal-modal" data-reveal>' , "\n";
				print '<h2>Are You Sure? That\'s a Huge step!</h2>' , "\n";
				print '<p>Stoping the service will cause unavailability of the system.</br>' , "\n";
				print 'Confirming rhat you want to <strong>stop the service</strong> will stop system.</p>' , "\n";
				print '<p><a href="#" data-reveal-id="stop_service_B" class="secondary button">Confirm</a></p>' , "\n";
				print '<a class="close-reveal-modal right">&#215;</a>' , "\n";
			print '</div>' , "\n";
			print '<div id="stop_service_B" class="reveal-modal" data-reveal>' , "\n";
				print '<h2>You Did It! You\'ve Set the Service to Halt!</h2>' , "\n";
				print '<p>Your system will stop! Good luck :)</p>' , "\n";
				print '<a class="close-reveal-modal">&#215;</a>' , "\n";
			print '</div>' , "\n";
			print '<!-- Reveal Modals begin STOP -->' , "\n";
			print '<div id="start_service" class="reveal-modal" data-reveal>' , "\n";
				print '<h2>Do You Want To Set It All On Motion?</h2>' , "\n";
				print '<p>Starting the service will activate the system.</br>' , "\n";
				print 'Confirming rhat you want to <strong>start the service</strong> will set it all on.</p>' , "\n";
				print '<p><a href="#" data-reveal-id="start_service_B" class="secondary button">Confirm</a></p>' , "\n";
				print '<a class="close-reveal-modal right">&#215;</a>' , "\n";
			print '</div>' , "\n";
			print '<div id="start_service_B" class="reveal-modal" data-reveal>' , "\n";
				print '<h2>Ignition! We Have Lift Off!</h2>' , "\n";
				print '<p>Your system will start now! Good luck :)</p>' , "\n";
				print '<a class="close-reveal-modal">&#215;</a>' , "\n";
			print '</div>' , "\n";
		print '</div>' , "\n";
	print '</aside>' , "\n";
}

sub print_load {
	local ($tit, $cont) = @_;
	return $cont;

}
sub _end 
{
	print '<script src="/unauthenticated/js/vendor/jquery.js"></script>' , "\n";
	print '<script src="/unauthenticated/js/foundation.min.js"></script>' , "\n";
	print '<script>' , "\n";
	print '$(document).foundation();' , "\n";
	print '</script>' , "\n";
	print '<script>' , "\n";
    print <<'ENDHTML';
   $(document).ready(function(){
	$('a[href*=#]').click(function() {
	  if (location.pathname.replace(/^\//,'') == this.pathname.replace(/^\//,'')
	  && location.hostname == this.hostname) {
	    var $target = $(this.hash);
	    $target = $target.length && $target
	    || $('[name=' + this.hash.slice(1) +']');
	    if ($target.length) {
	      var targetOffset = $target.offset().top;
	      $('html,body')
	      .animate({scrollTop: targetOffset}, 800);
	     return false;
	    }
	  }
	});
   });
ENDHTML
	print '</script>' , "\n";
}


#######################################################

sub print_menu_opener {
	print '<ul class="aside-nav">' . "\n";
	print '<li>' . "\n";
	print '<a href="#" data-open="hideMenu"><i class="fa fa-fw fa-bars"></i><span class="aside-text">Hide Menu</span></a>' . "\n";
	print '</li>' . "\n";
}
sub print_menu_category {
	local ($category, $label) = @_;
	use feature qw(switch);
	given($category) {
		when('webmin') { $icon = 'fa-cog'; }
		when('usermin') { $icon = 'fa-cog'; }
		when('system') { $icon = 'fa-wrench'; }
		when('servers') { $icon = 'fa-rocket'; }
		when('other') { $icon = 'fa-file'; }
		when('net') { $icon = 'fa-shield'; }
		when('info') { $icon = 'fa-info'; }
		when('hardware') { $icon = 'fa-hdd-o'; }
		when('cluster') { $icon = 'fa-power-off'; }
		when('unused') { $icon = 'fa-puzzle-piece'; }
		when('mail') { $icon = 'fa-envelope'; }
		when('login') { $icon = 'fa-user'; }
		when('apps') { $icon = 'fa-rocket'; }
		default { $icon = 'fa-cog'; }
	}
	print '<li>' . "\n";
	print '<a href="#" data-open="#' . $category . '">' . "\n";
	print '<i class="fa fa-fw ' . $icon . '"></i><span class="aside-text">' . $label . '<span class="aside-arrow" ><i class="fa fa-angle-right"></i></span></span>' . "\n";
	print '</a>' . "\n";
	print '</li>' . "\n";
}
sub print_menu_closer {
	print '</ul>' . "\n";
}
sub print_sub_category_opener {
	local ($id) = @_;
	print '<li class="submenu" id="' . $id . '">' . "\n";
	print '<ul class="aside-nav">' . "\n";
}
sub print_sub_category {
	local ($link, $label, $target) = @_;
	print '<li>' . "\n";
	print '<a href="' . $link .'" target="' . $target . '">' . $label . '</a>' . "\n";
	print '</li>' . "\n";
}
sub print_sub_category_closer {
	print '</ul>' . "\n";
	print '</li>' . "\n";
}
sub print_menu_search {
	print '<!--search-->' , "\n";
	print '<form class="search-aside" role="search" action="webmin_search.cgi" target="page-container">' . "\n";
	
	print '<div class="large-10 medium-10  columns">' , "\n";
    #print '<input type="text" placeholder="Find">' , "\n";
    print '<input class="form-control" name="search" placeholder="Search in ' . &get_product_name() . '" type="text">' . "\n";
    print '</div>' , "\n";
    
	print '<div class="large-2 medium-2  columns">' , "\n";
   # print '<a href="#" class="search button expand"><i class="fa fa-search fa-2x"></i></a>' , "\n";
    print '<input type="submit" value="Submit" class="search button expand">' , "\n";
    print '</div>' , "\n";
    
	print '</form>' . "\n";
}
sub print_menu_search_right_off {
	print '<!--search right off-->' , "\n";
	print '<form class="search-aside" role="search" action="webmin_search.cgi" target="page-container">' . "\n";
	print '<li class="show-for-small-only find"> ' , "\n";
	print '<a href="#" class="width25"><i class="fa fa-search fa-1x small-6"></i></a>' , "\n";
	print '<input type="text" class="small-6 width75" name="search" placeholder="Search in ' . &get_product_name() . '" >' , "\n";
	print '</li>' , "\n";
	print '</form>' . "\n";
}