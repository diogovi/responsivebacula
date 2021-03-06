#!/usr/bin/perl
# Drop several fields from a table

require './postgresql-lib.pl';
&ReadParse();
&error_setup($text{'fdrop_err'});
&can_edit_db($in{'db'}) || &error($text{'dbase_ecannot'});

# Validate inputs
@d = split(/\0/, $in{'d'});
@d || &error($text{'fdrop_enone'});
@desc = &table_structure($in{'db'}, $in{'table'});
@d < @desc || &error($text{'fdrop_eall'});

# Do the deed
foreach $d (@d) {
	&execute_sql_logged($in{'db'},
	    "alter table ".&quote_table($in{'table'})." drop column \"$d\"");
	}
&webmin_log("delete", "fields", scalar(@d), \%in);
&redirect("edit_table.cgi?db=$in{'db'}&table=".&urlize($in{'table'}));

