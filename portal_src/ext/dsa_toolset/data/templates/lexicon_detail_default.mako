<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>
<resource xmlns="http://www.wxwindows.org/wxxrc" version="2.3.0.1">
	<object class="wxPanel" name="lexicon_detail">
		<style>wxTAB_TRAVERSAL</style>
		<size>500,300</size>
		<object class="wxBoxSizer">
			<orient>wxVERTICAL</orient>
			<object class="sizeritem">
				<option>0</option>
				<flag>wxEXPAND</flag>
				<border>5</border>
				<object class="wxBoxSizer">
					<orient>wxHORIZONTAL</orient>
					<object class="sizeritem">
						<option>0</option>
						<flag></flag>
						<border>0</border>
						<object class="wxButton" name="lex_detail_group">
							<style>wxBU_EXACTFIT</style>
							<label>*</label>
							<default>0</default>
							<markup>0</markup>
							<bitmap />
						</object>
					</object>
					<object class="sizeritem">
						<option>0</option>
						<flag>wxALL</flag>
						<border>5</border>
						<object class="wxStaticText" name="m_staticText8">
							<label>Group: ${data.getparent().get('name')}</label>
							<wrap>-1</wrap>
						</object>
					</object>
				</object>
			</object>
			<object class="sizeritem">
				<option>1</option>
				<flag>wxALL|wxEXPAND</flag>
				<border>5</border>
				<object class="wxTextCtrl" name="m_textCtrl1">
					<style>wxTE_MULTILINE|wxTE_READONLY</style>
                    <value>${"".join([ "{:15}\t{}\n".format(a,v) for  a, v in data.attrib.items() ])}</value>
				</object>
			</object>
		</object>
	</object>
</resource>