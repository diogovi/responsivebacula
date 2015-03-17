#!/usr/bin/perl
BEGIN { push(@INC, ".."); };
use WebminCore;
&ReadParse();
&init_config();
if ($in{'mod'}) {
	$minfo = { &get_module_info($in{'mod'}) };
}
else {
	$minfo = &get_goto_module();
}
$goto = $minfo ? "$minfo->{'dir'}/" :
$in{'page-container'} ? "" : "body.cgi";

if ($minfo) {
	$cat = "?$minfo->{'category'}=1";
}
if ($in{'page-container'}) {
	$goto .= "/".$in{'page-container'};
}
%text = &load_language($current_theme);
%gaccess = &get_module_acl(undef, "");
$title = &get_html_framed_title();
&header($title);
print '<!-- Top bar/Nav e Side bar -->' , "\n";
print '<div class="off-canvas-wrap fixed" data-offcanvas>' , "\n";
print '<div class="inner-wrap">' , "\n";
print '<nav class="top-bar tab-bar">' , "\n";
print '<!-- Title -->' , "\n";

print '<div class="large-4 medium-4 small-4 columns ">' , "\n";
print '<ul class="title-area">' , "\n";
print '<li class="name row">' , "\n";
#print '<h1><a href="/"><span class="bacula-title">Webmin ' . &get_webmin_version() . '</span></a></h1>' , "\n";
print '<h1><a href="/"><span class="bacula-title">BACULA BACKUP</span></a></h1>' , "\n";
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
print '<!--list header-->' , "\n";
print '<li><label><i class="fa fa-refresh fa-1x center refresh right"></i></label></li>' , "\n";

print '<!--list body-->' , "\n";
=for comment
print '<li><a href="#">System hostname</a></li>' , "\n";
print '<li><a href="#">Operating system</a></li>' , "\n";
print '<li><a href="#">Webmin version</a></li>' , "\n";
print '<li><a href="#">CPU load averages</a></li>' , "\n";
print '<li><a href="#">Real memory</a></li>' , "\n";
print '<li><a href="#">Virtual memory</a></li>' , "\n";
print '<li><a href="#">Local disk space</a></li>' , "\n";
=cut

@cats = &get_visible_modules_categories();
@modules = map { @{$_->{'modules'}} } @cats;
foreach $cat (@cats) {
	&print_menu_category($cat->{'code'}, $cat->{'desc'});
	&print_sub_category_opener($cat->{'code'});
	foreach $module (@{$cat->{'modules'}}) {
		&print_sub_category($module->{'dir'} . '/', $module->{'desc'}, 'page-container');
	}
	&print_sub_category_closer();
}
if (-r "$root_directory/webmin_search.cgi" && $gaccess{'webminsearch'}) {
	#&print_menu_search_right_off();
}


=for comment
print '<li class="service_stats_button"><a href="#extreme"><span class="service"> Service Stats</span> <span class="fa fa-arrow-down fa-1x service right"></span></a></li>' , "\n";
print '</ul>	' , "\n";
print '<!-- Buttons -->	' , "\n";

print '<!-- Triggers the modals -->' , "\n";

print '<div id="extreme" class="large-12 medium-12 small-12 restart_block">' , "\n";

print '<div class="large-4 medium-4 small-4 left"><a href="#" data-reveal-id="restart_service" class="button restart_bacula">Restart Bacula</a></div> ' , "\n";
print '<div class="large-4 medium-4 small-4 left"><a href="#" data-reveal-id="stop_service" class="button restart_bacula">Stop Bacula</a></div>' , "\n";
print '<div class="large-4 medium-4 small-4 left"><a href="#" data-reveal-id="start_service" class="button restart_bacula">Start at Boot</a></div>' , "\n";

print '<div class="large-12 medium-12 small-12 show-for-small-only left vi_logo_side">' , "\n";
print '<a href="http://www.versaointegral.pt"><img class="vi_logo"  src="img/logos/vi_logo.png" alt="Versão Integral"/></a>' , "\n";
print '<a href="http://www.versaointegral.pt"><img class="vi_logo" src="' . $gconfig{'webprefix'} . 'unauthenticated/img/logos/vi_logo.png" alt="Versao Integral"/></a>' , "\n";
print '</div>' , "\n";

print '</div>' , "\n";

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
print '</div>' , "\n";

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
=cut

#print '</div>' , "\n";
print '</aside>' , "\n";

print '<div class="iframe-container">' . "\n";
print '<iframe name="page-container" src="' . $goto . '">' . "\n";
#print '<object name="page-container" type="text/html" data="' . $goto . '"></object>' . "\n";
print '</iframe>' . "\n";
print '</div>' . "\n";

print '<a class="exit-off-canvas"></a>' , "\n";

print '<footer>' , "\n";
print '<div class="large-12 medium-12 small-12">' , "\n";

print '<div class="large-3 medium-4 hide-for-small-only columns">' , "\n";
print '<a href="http://www.versaointegral.pt"><img class="vi_logo" src="' . $gconfig{'webprefix'} . 'unauthenticated/img/logos/vi_logo.png" alt="Versao Integral"/></a>' , "\n";
print '</div>' , "\n";

print '<div class="large-7 medium-4 small-8 columns user">' , "\n";
#print 'Admnin@192.168.2.210' , "\n";
$user = $remote_user;
if (&foreign_available("net")) {
	$user = '<a data-toggle="collapse" data-target="#navbar-collapse" target="page-container" href="' . $gconfig{'webprefix'} . '/acl/edit_user.cgi?user=' . $user .'">' . $user . '</a>';
}
#print '<p class="navbar-text pull-right">Welcome, ' . $user . '</p>' . "\n";
print '<h3>Welcome, ' . $user . '@' . &get_display_hostname() . "</h3>\n";
print '</div>' , "\n";

print '<!-- Logout -->' , "\n";
#print '<a href="login.html"><div class="large-2 medium-4 small-4 columns logout">logout</div></a>' , "\n";
&get_miniserv_config(\%miniserv);
if ($miniserv{'logout'} && !$ENV{'SSL_USER'} && !$ENV{'LOCAL_USER'} && $ENV{'HTTP_USER_AGENT'} !~ /webmin/i) {
	if ($main::session_id) {
		print '<a href="'. $gconfig{'webprefix'} . '/session_login.cgi?logout=1" class="btn btn-danger navbar-btn pull-right"><i class="fa fa-sign-out"></i> Logout</a>' . "\n";
	} else {
		print '<a href="switch_user.cgi" class="btn btn-danger navbar-btn pull-right"> Switch user</a>' . "\n";
	}
}

print '</div>' , "\n";

print '</footer>  ' , "\n";
print '</div>' , "\n";

print '<!--##############################################################################################################-->' , "\n";	
	print "</div>\n";
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