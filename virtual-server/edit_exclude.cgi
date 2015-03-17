#!/usr/bin/perl
# Show per-domain excluded directories

require './virtual-server-lib.pl';
&ReadParse();
$d = &get_domain($in{'dom'});
&can_edit_domain($d) || &error($text{'edit_ecannot'});
&can_edit_exclude() || &error($text{'exclude_ecannot'});

&ui_print_header(&domain_in($d), $text{'exclude_title'}, "");

print $text{'exclude_desc'},"<p>\n";

print &ui_form_start("save_exclude.cgi");
print &ui_hidden("dom", $d->{'id'}),"\n";
print &ui_table_start($text{'exclude_header'}, undef, 2);

@exclude = &get_backup_excludes($d);
print &ui_table_row($text{'exclude_dirs'},
		    &ui_textarea("dirs", join("\n", @exclude)."\n", 5, 50).
		    " ".&file_chooser_button("dirs", 1, undef, $d->{'home'},1));

print &ui_table_end();
print &ui_form_end([ [ "save", $text{'save'} ] ]);

&ui_print_footer(&domain_footer_link($d),
		 "", $text{'index_return'});

