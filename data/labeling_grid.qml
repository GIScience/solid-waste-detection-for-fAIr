<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="3.34" styleCategories="Symbology">
  <renderer-v2 type="RuleRenderer" symbollevels="0" referencescale="-1" forceraster="0" enableorderby="0">
    <rules key="{rules}">
      <rule key="{unlabeled}" label="unlabeled" filter="&quot;label&quot; IS NULL" symbol="0"/>
      <rule key="{waste}" label="waste (label=1)" filter="&quot;label&quot; = 1" symbol="1"/>
      <rule key="{background}" label="background (label=0)" filter="&quot;label&quot; = 0" symbol="2"/>
    </rules>
    <symbols>
      <symbol type="fill" name="0" alpha="1" clip_to_extent="1" force_rhr="0">
        <layer class="SimpleFill" enabled="1" pass="0" locked="0">
          <prop k="color" v="255,255,255,0"/>
          <prop k="outline_color" v="255,216,0,255"/>
          <prop k="outline_width" v="0.25"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="style" v="no"/>
        </layer>
      </symbol>
      <symbol type="fill" name="1" alpha="0.45" clip_to_extent="1" force_rhr="0">
        <layer class="SimpleFill" enabled="1" pass="0" locked="0">
          <prop k="color" v="230,0,0,180"/>
          <prop k="outline_color" v="120,0,0,255"/>
          <prop k="outline_width" v="0.20"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="style" v="solid"/>
        </layer>
      </symbol>
      <symbol type="fill" name="2" alpha="0.30" clip_to_extent="1" force_rhr="0">
        <layer class="SimpleFill" enabled="1" pass="0" locked="0">
          <prop k="color" v="0,120,255,120"/>
          <prop k="outline_color" v="0,60,140,255"/>
          <prop k="outline_width" v="0.20"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="style" v="solid"/>
        </layer>
      </symbol>
    </symbols>
  </renderer-v2>
  <layerGeometryType>2</layerGeometryType>
</qgis>
