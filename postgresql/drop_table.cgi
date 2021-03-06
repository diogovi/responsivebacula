#!/usr/bin/perl
# drop_table.cgi
# Delete an existing table

require './postgresql-lib.pl';
&ReadParse();
&can_edit_db($in{'db'}) || &error($text{'dbase_ecannot'});
$qt = &quote_table($in{'table'});
if ($in{'confirm'}) {
	# Drop the table
	&error_setup($text{'tdrop_err'});
	&execute_sql_logged($in{'db'}, "drop table $qt");
	&webmin_log("delete", "table", $in{'table'}, \%in);
	&redirect("edit_dbase.cgi?db=$in{'db'}");
	}
else {
	# Ask the user if he is sure..
	&ui_print_header(undef, $text{'tdrop_title'}, "");
	@tables = &list_tables($in{'db'});
	$d = &execute_sql_safe($in{'db'}, "select count(*) from $qt");
	$rows = $d->{'data'}->[0]->[0];

	print "<center><b>", &text('tdrop_rusure', "<tt>$in{'table'}</tt>",
				   "<tt>$in{'db'}</tt>", $rows),"</b><p>\n";
	print "<form action=drop_table.cgi>\n";
	print "<input type=hidden name=db value='$in{'db'}'>\n";
	print "<input type=hidden name=table value='$in{'table'}'>\n";
	print "<input type=submit name=confirm value='$text{'tdrop_ok'}'>\n";
	print "</form></center>\n";
	&ui_print_footer("edit_table.cgi?db=$in{'db'}&table=$in{'table'}",
		$text{'table_return'});
	}

