sub theme_header {
	print '<!DOCTYPE HTML>' , "\n";
	print '<html>' , "\n";
	print '<head>' , "\n";
	print '<title>' , $_[0] , '</title>' , "\n";
	print '<meta charset="utf-8">' , "\n";
	print '<meta name="viewport" content="width=device-width, initial-scale=1.0">' , "\n";
	
	print '<link href="'. $gconfig{'webprefix'} . '/unauthenticated/css/foundation.css" rel="stylesheet" type="text/css">' , "\n";
	print '<link href="'. $gconfig{'webprefix'} . '/unauthenticated/css/responsivebacula.css" rel="stylesheet" type="text/css">' , "\n";
	print '<link href="'. $gconfig{'webprefix'} . '/unauthenticated/font-awesome/css/font-awesome.min.css" rel="stylesheet" type="text/css">' , "\n";
	print '<script src="'. $gconfig{'webprefix'} . '/unauthenticated/js/vendor/modernizr.js" type="text/javascript"></script>' , "\n";
	#print '<link href="'. $gconfig{'webprefix'} . '/css/webmin.css" rel="stylesheet" type="text/css">' , "\n";
	
	#print '<link href="'. $gconfig{'webprefix'} . '/css/bootstrap.css" rel="stylesheet" type="text/css">' , "\n";
	

	#print '<link href="'. $gconfig{'webprefix'} . '/css/fontawesome.css" rel="stylesheet" type="text/css">' , "\n";
	#print '<link href="'. $gconfig{'webprefix'} . '/css/circleprogress.css" rel="stylesheet" type="text/css">' , "\n";
	print '<script src="'. $gconfig{'webprefix'} . '/js/jquery.js" type="text/javascript"></script>' , "\n";
	print '<script src="'. $gconfig{'webprefix'} . '/js/bootstrap.js" type="text/javascript"></script>' , "\n";
	#print '<script src="'. $gconfig{'webprefix'} . '/js/webmin.js" type="text/javascript"></script>' , "\n";
	print '</head>' , "\n";
	print '<body>' , "\n";
	
if (@_ > 1) {
	print '<div class="container">' . "\n";
	my %this_module_info = &get_module_info(&get_module_name());
	print '<div class="panel panel-default" style="margin-top: 20px">' . "\n";
	print '<div class="panel-heading">' . "\n";
	print "<div class='header' width=100%><div>\n";


	print '<div class="panel-body">' . "\n";
	}
	$miniserv::page_capture = 1;
}
sub theme_footer {
#for(my $i=0; $i+1<@_; $i+=2) {
#	my $url = $_[$i];
#	if ($url ne '/' || !$tconfig{'noindex'}) {
#		if ($url eq '/') {
#			$url = "/?cat=$this_module_info{'category'}";
#			}
#		elsif ($url eq '' && &get_module_name()) {
#			$url = "/".&get_module_name()."/".
#			       $this_module_info{'index_link'};
#			}
#		elsif ($url =~ /^\?/ && &get_module_name()) {
#			$url = "/".&get_module_name()."/$url";
#			}
#		$url = "$gconfig{'webprefix'}$url" if ($url =~ /^\//);
#		print "&nbsp;<a style='margin-bottom: 15px;' class='btn btn-primary' href=\"$url\"><i class='fa fa-arrow-left'></i> ",&text('main_return', $_[$i+1]),"</a>\n";
#		}
#	}
	#If you comment this </div>, decomment the </div> commented in theme_ui_pre_footer, index.cgi, body.cgi


	print '</body>' , "\n";
	print '</html>' , "\n";
}
sub theme_file_chooser_button
{
my $form = defined($_[2]) ? $_[2] : 0;
my $chroot = defined($_[3]) ? $_[3] : "/";
my $add = int($_[4]);
my ($w, $h) = (400, 300);
if ($gconfig{'db_sizefile'}) {
	($w, $h) = split(/x/, $gconfig{'db_sizefile'});
	}
return "<button class='btn btn-default' type=button onClick='ifield = form.$_[0]; chooser = window.open(\"$gconfig{'webprefix'}/chooser.cgi?add=$add&type=$_[1]&chroot=$chroot&file=\"+escape(ifield.value), \"chooser\", \"toolbar=no,menubar=no,scrollbars=no,resizable=yes,width=$w,height=$h\"); chooser.ifield = ifield; window.ifield = ifield'>...</button>\n";
}
sub theme_popup_window_button
{
my ($url, $w, $h, $scroll, $fields) = @_;
my $scrollyn = $scroll ? "yes" : "no";
my $rv = "<input class='btn btn-default' type=button onClick='";
foreach my $m (@$fields) {
	$rv .= "$m->[0] = form.$m->[1]; ";
	}
my $sep = $url =~ /\?/ ? "&" : "?";
$rv .= "chooser = window.open(\"$url\"";
foreach my $m (@$fields) {
	if ($m->[2]) {
		$rv .= "+\"$sep$m->[2]=\"+escape($m->[0].value)";
		$sep = "&";
		}
	}
$rv .= ", \"chooser\", \"toolbar=no,menubar=no,scrollbars=$scrollyn,resizable=yes,width=$w,height=$h\"); ";
foreach my $m (@$fields) {
	$rv .= "chooser.$m->[0] = $m->[0]; ";
	$rv .= "window.$m->[0] = $m->[0]; ";
	}
$rv .= "' value=\"...\">";
return $rv;
}
sub theme_ui_upload
{
my ($name, $size, $dis, $tags) = @_;
$size = &ui_max_text_width($size);
return "<input style='margin: 4px 0;' class='ui_upload' type=file name=\"".&quote_escape($name)."\" ".
       "size=$size ".
       ($dis ? "disabled=true" : "").
       ($tags ? " ".$tags : "").">";
}

# Thi is the web-lib-funcs.pl part dedicated to all web lib functions.
# WARNING!!! Work in progress - Not all is implemented!!!

################################# Theme icons generation functions #################################

# ff
sub theme_icons_table {
	print '<div class="row icons-row">' , "\n";
	for(my $i=0; $i<@{$_[0]}; $i++) {
		print '<div style="text-align: center;" class="col-xs-6 col-sm-4 col-md-3">' , "\n";
		&generate_icon($_[2]->[$i], $_[1]->[$i], $_[0]->[$i], ref($_[4]) ? $_[4]->[$i] : $_[4], $_[5], $_[6], $_[7]->[$i], $_[8]->[$i]);
		print '</div>' , "\n";
	}
	print '</div>' , "\n";
}

sub theme_generate_icon {
	my ($icon, $title, $link, $href, $width, $height, $before, $after) = @_;
	# Decomment only when new icons are ready
	# $icon =~ s/.gif/.png/;
	$width = !defined($width) ? '48' : $width;
	$height = !defined($height) ? '48' : $height;

	if ($tconfig{'noicons'}) {
		if ($link) {
			print '<div>';
			print $before;
			print '<a href="' . $link . '" ' . $href . '>' . $title . '</a>';
			print $after;
			print '</div>';
		} else {
			print '<div>';
			print $before;
			print $title;
			print $after;
			print '</div>';
		}
	} elsif ($link) {
		print '<div style="height: 120px;" class="icon-container">';
		print '<a href="' . $link . '" ' . $href . '><img style="padding: 7px; border-radius: 4px; border: 1px solid #DDD; background: linear-gradient(to bottom, #FCFCFC 0%, #F5F5F5 100%) repeat scroll 0% 0% transparent; width: 64px; height: 64px; box-shadow: 0px 1px 1px rgba(0, 0, 0, 0.05);" src="' . $icon . '" width="' . $width . '" height="' . $height . '">';
		print $before;
		print '<a href="' . $link . '" ' . $href . '><p>' . $title . '</p></a>';
		print $after;
		print '</div>';
	} else {
		print '<div class="icon-container">';
		print '<img style="padding: 7px; border-radius: 4px; border: 1px solid #DDD; background: linear-gradient(to bottom, #FCFCFC 0%, #F5F5F5 100%) repeat scroll 0% 0% transparent; width: 64px; height: 64px; box-shadow: 0px 1px 1px rgba(0, 0, 0, 0.05);" src="' . $icon . '" width="' . $width . '" height="' . $height . '">';
		print $before;
		print '<p>' . $title . '</p>';
		print $after;
		print '</div>';
	}
}

# Thi is the theme.pl part dedicated to all theme functions.
# WARNING!!! Work in progress - Not all is implemented!!!
# All the # theme_ui_x are are not yet implemented theme functions.

################################# Theme table generation functions #################################

# theme_ui_table_start

# theme_ui_table_end

# theme_ui_table_row

# theme_ui_table_hr

# theme_ui_table_span

sub theme_ui_columns_start {
	my ($heads, $width, $noborder, $tdtags, $title) = @_;
	my ($rv, $i);

	$rv .= '<table class="table table-striped table-rounded">' , "\n";
	$rv .= '<thead>' , "\n";
	$rv .= '<tr>' , "\n";
	for($i=0; $i<@$heads; $i++) {
		$rv .= '<th>';
		$rv .= ($heads->[$i] eq '' ? '<br>' : $heads->[$i]);
		$rv .= '</th>' , "\n";
	}
	$rv .= '</tr>' , "\n";
	$rv .= '</thead>' , "\n";

	return $rv;
}

sub theme_ui_columns_row {
	my ($cols, $tdtags) = @_;
	my ($rv, $i);

	#$rv .= '<tbody>' , "\n";
	$rv .= '<tr>' , "\n";
	for($i=0; $i<@$cols; $i++) {
		$rv .= '<td>' , "\n";
		$rv .= ($cols->[$i] !~ /\S/ ? '<br>' : $cols->[$i]);
		$rv .= '</td>' , "\n";
	}
	$rv .= '</tr>' , "\n";
	#$rv .= '</tbody>' , "\n";

	return $rv;
}

sub theme_ui_columns_header {
	my ($cols, $tdtags) = @_;
	my ($rv, $i);

	$rv .= '<thead>' , "\n";
	$rv .= '<tr>' , "\n";
	for($i=0; $i<@$cols; $i++) {
		$rv .= '<th>';
		$rv .= ($cols->[$i] eq '' ? '#' : $cols->[$i]);
		$rv .= '</th>' , "\n";
	}
	$rv .= '</tr>' , "\n";
	$rv .= '</thead>' , "\n";

	return $rv;
}

# theme_ui_checked_columns_row

# theme_ui_radio_columns_row

sub theme_ui_columns_end {
	my $rv;

	$rv .= '</table>' , "\n";

	return $rv;
}

# theme_ui_columns_table

# theme_ui_form_columns_table

################################# Theme form generation functions #################################

sub theme_ui_form_start {
	my ($script, $method, $target, $tags) = @_;
	my $rv;

	$rv .= '<form role="form" ';
	$rv .= 'action="' . &html_escape($script) . '" ';
	$rv .= ($method eq 'post' ? 'method="post" ' : $method eq 'form-data' ? 'method="post" enctype="multipart/form-data" ' : 'method="get" ');
	$rv .= ($target ? 'target="' . $target . '" ' : '');
	$rv .= ($tags ? $tags : '');
	$rv .= '>' , "\n";

	return $rv;
}

# theme_ui_form_end

sub theme_ui_textbox {
	my ($name, $value, $size, $dis, $max, $tags) = @_;
	my $rv;

	$rv .= '<input style="display: inline; width: auto;" class="form-control" type="text" ';
	$rv .= 'name="' . &quote_escape($name) . '" ';
	$rv .= 'value="' . &quote_escape($value) . '" ';
	$rv .= 'size="' . $size . '" ';
	$rv .= ($dis ? 'disabled="true" ' : '');
	$fv .= ($max ? 'maxlength="' . $max . '" ' : '');
	$rv .= ($tags ? $tags : '');
	$rv .= '>' , "\n";

	return $rv;
}

# theme_ui_filebox

# theme_ui_upload

sub theme_ui_password {
	my ($name, $value, $size, $dis, $max, $tags) = @_;
	my $rv;

	$rv .= '<input style="display: inline; width: auto;" class="form-control" type="password" ';
	$rv .= 'name="' . &quote_escape($name) . '" ';
	$rv .= 'value="' . &quote_escape($value) . '" ';
	$rv .= 'size="' . $size . '" ';
	$rv .= ($dis ? 'disabled="true" ' : '');
	$fv .= ($max ? 'maxlength="' . $max . '" ' : '');
	$rv .= ($tags ? $tags : '');
	$rv .= '>' , "\n";

	return $rv;
}

# theme_ui_hidden

# theme_ui_select

# theme_ui_multi_select

# theme_ui_multiselect_javascript

# theme_ui_yesno_radio 

# theme_ui_checkbox 

# theme_ui_oneradio

sub theme_ui_textarea {
	my ($name, $value, $rows, $cols, $wrap, $dis, $tags) = @_;
	my $rv;
	$cols = &ui_max_text_width($cols, 1);

	$rv .= '<textarea style="display: inline; width: auto;" class="form-control" ';
	$rv .= 'name="' . &quote_escape($name) . '" ';
	$rv .= 'rows="' . $rows . '" ';
	$rv .= 'cols="' . $cols . '" ';
	$rv .= ($wrap ? 'wrap="' . $wrap . '" ' : '');
	$rv .= ($dis ? 'disabled="true" ' : '');
	$rv .= ($tags ? $tags : '');
	$rv .= '>' , "\n";
	$rv .= &html_escape($value) , "\n";
	$rv .= '</textarea>' , "\n";

	return $rv;
}

# theme_ui_user_textbox

# theme_ui_group_textbox

# theme_ui_opt_textbox

sub theme_ui_submit {
	my ($label, $name, $dis, $tags) = @_;
	my ($rv, $fa);
	my $btntype = 'btn-default';

	if ($name eq 'delete') {
		$btntype = 'btn-danger';
		#$fa = '<i class="fa fa-times"></i>';
	} elsif ($name eq 'stop') {
		$btntype = 'btn-danger';
		#$fa = '<i class="fa fa-exclamation"></i>';
	} elsif ($name eq 'start') {
		$btntype = 'btn-success';
		#$fa = '<i class="fa fa-check"></i>';
	} elsif ($name eq 'restart') {
		$btntype = 'btn-warning';
		#$fa = '<i class="fa fa-refresh"></i>';
	}

	$rv .= '<button type="submit" class="btn ' . $btntype . '" ';
	$rv .= ($name ne '' ? 'name="' . &quote_escape($name) . '" ' : '');
	$rv .= ($name ne '' ? 'id="' . &quote_escape($name) . '" ' : '');
	$rv .= ' value="' . &quote_escape($label) . '"'.
	$rv .= ($dis ? ' disabled="disabled"' : '');
	$rv .= ($tags ? ' ' . $tags : ''). '>';
	$rv .= $fa . ' ' . &quote_escape($label);
	$rv .= '</button>' , "\n";

	return $rv;
}

sub theme_ui_reset {
	my ($label, $dis) = @_;
	my $rv;

	$rv .= '<button class="btn btn-default" type="reset" ';
	$rv .= ($dis ? 'disabled="disabled">' : '>');
	$rv .= &quote_escape($label);
	$rv .= '</button>' , "\n";

	return $rv;
}

sub theme_ui_button {
	my ($label, $name, $dis, $tags) = @_;
	my $rv;

	$rv .= '<button type="button" class="btn btn-default" ';
	$rv .= ($name ne '' ? 'name="' . &quote_escape($name) . '" ' : '');
	$rv .= ($dis ? 'disabled="disabled"' : '');
	$rv .= ($tags ? ' ' . $tags : ''). '>';
	$rv .= &quote_escape($label);
	$rv .= '</button>' , "\n";

	return $rv;
}

# theme_ui_date_input

sub theme_ui_buttons_start {
	return "<div class='ui_buttons_table'>\n";
}

sub theme_ui_buttons_end {
	return "</div>\n";
}

# theme_ui_buttons_row
sub theme_ui_buttons_row
{

my ($script, $label, $desc, $hiddens, $after, $before) = @_;
if (ref($hiddens)) {
	$hiddens = join("\n", map { &ui_hidden(@$_) } @$hiddens);
	}
return "<form action='$script' class='ui_buttons_form'>\n".
       $hiddens.
     #  "<tr class='ui_buttons_row'> ".
       "<div class=ui_buttons_label>".
       ($before ? $before." " : "").
       &ui_submit($label).($after ? " ".$after : "")."</div>\n".
       "<div class=ui_buttons_value>".
       $desc."</div></div>\n".
       "</form>\n";
}
# theme_ui_buttons_hr
sub theme_ui_buttons_hr
{
my ($title) = @_;
if ($title) {
	return "<div'ui_buttons_hr'><div><div><div><div><hr></div><div>$title</div><div><hr></div></div></div></div></div>\n";
	}
else {
	return "<div class='ui_buttons_hr'><div><hr></div></div>\n";
	}
}
################################# Theme header and footer functions #################################

sub theme_ui_post_header {
	my ($text) = @_;

	my $rv;
	#$rv .= '<hr>' , "\n";

	return $rv;
}

sub theme_ui_pre_footer {
	my $rv;
	$rv .= '</div>' , "\n";
	$rv .= '</div>' , "\n";
	return $rv;
}

sub theme_ui_print_header
{
	my ($text, @args) = @_;
	&header(@args);
	#print &ui_post_header($text);
}

# theme_ui_print_unbuffered_header

sub theme_ui_print_footer
{
	#print '<a class="exit-off-canvas"></a>' , "\n";
	print '<footer>' , "\n";
	print '<div class="large-12 medium-12 small-12">' , "\n";
	print '<div class="large-3 medium-4 hide-for-small-only columns">' , "\n";
	print '<a href="http://www.versaointegral.pt"><img class="vi_logo" src="' . $gconfig{'webprefix'} . '/unauthenticated/img/logos/vi_logo.png" alt="Versao Integral"/></a>' , "\n";
	print '</div>' , "\n";
	print '<div class="large-7 medium-4 small-8 columns user">' , "\n";
	$user = $remote_user;
	if (&foreign_available("net")) {
		$user = '<a data-toggle="collapse" data-target="#navbar-collapse" target="page-container" href="' . $gconfig{'webprefix'} . '/acl/edit_user.cgi?user=' . $user .'">' . $user . '</a>';
	}
	print '<div class="large-7 medium-4 small-8 columns user">' . $user . '@' . &get_display_hostname() . "</div>\n";
#	print '</div>' , "\n";
	print '<!-- Logout -->' , "\n";
	&get_miniserv_config(\%miniserv);
	if ($miniserv{'logout'} && !$ENV{'SSL_USER'} && !$ENV{'LOCAL_USER'} && $ENV{'HTTP_USER_AGENT'} !~ /webmin/i) {
		if ($main::session_id) {
			print '<a href="'. $gconfig{'webprefix'} . '/session_login.cgi?logout=1" class="large-2 medium-4 small-4 columns logout">logout</a>' . "\n";
		} else {
			print '<a href="switch_user.cgi" class="large-2 medium-4 small-4 columns logout"> Switch user</a>' . "\n";
		}
	}
	print '</div>' , "\n";
	print '</footer> ' , "\n";
	print '</div>' , "\n";
	print '<!--##########################################################-->' , "\n";	
	print '</div>',"\n";
}

# theme_ui_config_link

# theme_ui_print_endpage

# theme_ui_subheading
sub theme_ui_subheading 
{
	$hed = '<div class="large-12 medium-12 small-12 columns main-tittle text-center primeiro titulo arrow_box">'.join("", @_).'</div>';
	#return "<h1 class='ui_subheading'>".join("", @_)."</h1>\n";
	return $hed;
}

# theme_ui_links_row

################################# Theme collapsible section / tab functions #################################

# theme_ui_hidden_javascript

# theme_ui_hidden_start

# theme_ui_hidden_end

# theme_ui_hidden_table_row_start

# theme_ui_hidden_table_row_end

# theme_ui_hidden_table_start

# theme_ui_hidden_table_end

sub theme_ui_tabs_start {
	my ($tabs, $name, $sel, $border) = @_;
	my $rv;

	$rv .= '<ul class="nav nav-tabs">' , "\n";
	foreach my $t (@$tabs) {
		my $tabid = "tab_".$t->[0];
		if ($t->[0] eq $sel) {
			$rv .= '<li class="active"><a data-toggle="tab" href="#' . $t->[0] . '">' . $t->[1] . '</a></li>' , "\n";
		} else {
			$rv .= '<li><a data-toggle="tab" href="#' . $t->[0] . '">' . $t->[1] . '</a></li>' , "\n";
		}
	}
	$rv .= '</ul>' , "\n";
	$rv .= '<div class="tab-content">' , "\n";
	$main::ui_tabs_selected = $sel;

	return $rv;
}

sub theme_ui_tabs_end {
	my ($border) = @_;
	my $rv;

	$rv .= '</div>' , "\n";

	return $rv;
}

sub theme_ui_tabs_start_tab {
	my ($name, $tab) = @_;
	my $rv;
	my $defclass = $tab eq $main::ui_tabs_selected ? 'active' : '';

	$rv .= '<div id="' . $tab . '" class="tab-pane ' . $defclass . '">' , "\n";

	return $rv;
}

# theme_ui_tabs_start_tabletab

sub theme_ui_tabs_end_tab {
	my $rv;

	$rv .= '</div>' , "\n";

	return $rv;
}

# theme_ui_tabs_end_tabletab

# theme_ui_radio_selector

################################# Theme collapsible section / tab functions #################################

# theme_ui_grid_table

# theme_ui_radio_table

# theme_ui_up_down_arrows

sub theme_ui_hr {
	my $rv;

	$rv .= '<hr>' , "\n";

	return $rv;
}

# theme_ui_nav_link

# theme_ui_confirmation_form !!!!! NB: Not available to override ?????

sub theme_ui_alert_box {
	my ($msg, $class) = @_;
	my ($rv, $type, $tmsg, $fa);

	if ($class eq "success") { $type = 'alert-success', $tmsg = 'Well done!', $fa = 'fa-check'; }
	elsif ($class eq "info") { $type = 'alert-info', $tmsg = 'Heads up!', $fa = 'fa-info'; }
	elsif ($class eq "warn") { $type = 'alert-warning', $tmsg = 'Warning!', $fa = 'fa-exclamation-triangle'; }
	elsif ($class eq "danger") { $type = 'alert-danger', $tmsg = 'Oh snap!', $fa = 'fa-bolt'; }

	$rv .= '<div class="alert ' . $type . '">' , "\n";
	$rv .= '<i class="fa fa-fw ' . $fa . '"></i> <strong>' . $tmsg . '</strong>';
	$rv .= '<br>' , "\n";
	$rv .= $msg , "\n";
	$rv .= '</div>' , "\n";

	return $rv;
}

# theme_ui_page_flipper

# theme_js_redirect
