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
				<option>0</option>
				<flag>wxALL</flag>
				<border>5</border>
				<object class="wxStaticText" name="m_staticText1">
					<font>
						<size>20</size>
						<style>normal</style>
						<weight>bold</weight>
						<underlined>0</underlined>
					</font>
					<label>${data.get('name')}</label>
					<wrap>-1</wrap>
				</object>
			</object>
			<object class="sizeritem">
				<option>0</option>
				<flag>wxEXPAND</flag>
				<border>5</border>
				<object class="wxBoxSizer">
					<orient>wxHORIZONTAL</orient>
					<object class="sizeritem">
						<option>0</option>
						<flag>wxALL</flag>
						<border>5</border>
						<object class="wxStaticText" name="m_staticText2">
							<label>Preis:</label>
							<wrap>-1</wrap>
						</object>
					</object>
					<object class="sizeritem">
						<option>0</option>
						<flag>wxALL</flag>
						<border>5</border>
						<object class="wxStaticText" name="m_staticText3">
							<label>${"{} {}".format(data.get('price'),data.get('price_unit'))}</label>
							<wrap>-1</wrap>
						</object>
					</object>
					<object class="sizeritem">
						<option>0</option>
						<flag>wxLEFT|wxTOP</flag>
						<border>5</border>
						<object class="wxStaticText" name="m_staticText5">
							<font>
								<style>normal</style>
								<weight>bold</weight>
								<underlined>0</underlined>
							</font>
							<%
							    s_price = "Spezial: " + data.get('s_price') if data.get('s_price') is not None else ''
							    s_price_unit = data.get('s_price_unit') if data.get('s_price_unit') is not None else ''
							%>
							<label>${"{} {}".format(s_price, s_price_unit)}</label>
							<wrap>-1</wrap>
						</object>
					</object>
				</object>
			</object>
			<object class="sizeritem">
				<option>0</option>
				<flag>wxEXPAND</flag>
				<border>5</border>
				<object class="wxBoxSizer">
					<orient>wxHORIZONTAL</orient>
					<object class="sizeritem">
						<option>0</option>
						<flag>wxALL</flag>
						<border>5</border>
						<object class="wxStaticText" name="m_staticText6">
							<label>Gewicht:</label>
							<wrap>-1</wrap>
						</object>
					</object>
					<object class="sizeritem">
						<option>0</option>
						<flag>wxALL</flag>
						<border>5</border>
						<object class="wxStaticText" name="m_staticText7">
							<label>${"{}".format(data.get('weight'))}</label>
							<wrap>-1</wrap>
						</object>
					</object>
				</object>
			</object>
		</object>
	</object>
</resource>