<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="3.24.0-Tisler" styleCategories="AllStyleCategories" minScale="1e+08" hasScaleBasedVisibilityFlag="0" maxScale="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
    <Private>0</Private>
  </flags>
  <temporal mode="0" fetchMode="0" enabled="0">
    <fixedRange>
      <start></start>
      <end></end>
    </fixedRange>
  </temporal>
  <customproperties>
    <Option type="Map">
      <Option value="Value" name="identify/format" type="QString"/>
    </Option>
  </customproperties>
  <pipe-data-defined-properties>
    <Option type="Map">
      <Option value="" name="name" type="QString"/>
      <Option name="properties"/>
      <Option value="collection" name="type" type="QString"/>
    </Option>
  </pipe-data-defined-properties>
  <pipe>
    <provider>
      <resampling zoomedInResamplingMethod="cubic" enabled="false" maxOversampling="2" zoomedOutResamplingMethod="cubic"/>
    </provider>
    <rasterrenderer nodataColor="" classificationMax="55" classificationMin="-1.5" alphaBand="-1" type="singlebandpseudocolor" band="1" opacity="1">
      <rasterTransparency/>
      <minMaxOrigin>
        <limits>None</limits>
        <extent>WholeRaster</extent>
        <statAccuracy>Estimated</statAccuracy>
        <cumulativeCutLower>0.02</cumulativeCutLower>
        <cumulativeCutUpper>0.98</cumulativeCutUpper>
        <stdDevFactor>2</stdDevFactor>
      </minMaxOrigin>
      <rastershader>
        <colorrampshader maximumValue="55" classificationMode="1" labelPrecision="0" clip="0" colorRampType="INTERPOLATED" minimumValue="-1.5">
          <colorramp name="[source]" type="gradient">
            <Option type="Map">
              <Option value="0,30,80,255" name="color1" type="QString"/>
              <Option value="155,123,98,255" name="color2" type="QString"/>
              <Option value="ccw" name="direction" type="QString"/>
              <Option value="0" name="discrete" type="QString"/>
              <Option value="gradient" name="rampType" type="QString"/>
              <Option value="rgb" name="spec" type="QString"/>
              <Option value="0.00353982;0,51,102,255;rgb;ccw:0.00707965;0,102,153,255;rgb;ccw:0.0106195;0,153,205,255;rgb;ccw:0.0159292;100,200,255,255;rgb;ccw:0.0212389;198,236,255,255;rgb;ccw:0.0265487;148,171,132,255;rgb;ccw:0.20354;172,191,139,255;rgb;ccw:0.380531;189,204,150,255;rgb;ccw:0.557522;228,223,175,255;rgb;ccw:0.734513;230,202,148,255;rgb;ccw:0.823009;205,171,131,255;rgb;ccw:0.911504;181,152,128,255;rgb;ccw" name="stops" type="QString"/>
            </Option>
            <prop v="0,30,80,255" k="color1"/>
            <prop v="155,123,98,255" k="color2"/>
            <prop v="ccw" k="direction"/>
            <prop v="0" k="discrete"/>
            <prop v="gradient" k="rampType"/>
            <prop v="rgb" k="spec"/>
            <prop v="0.00353982;0,51,102,255;rgb;ccw:0.00707965;0,102,153,255;rgb;ccw:0.0106195;0,153,205,255;rgb;ccw:0.0159292;100,200,255,255;rgb;ccw:0.0212389;198,236,255,255;rgb;ccw:0.0265487;148,171,132,255;rgb;ccw:0.20354;172,191,139,255;rgb;ccw:0.380531;189,204,150,255;rgb;ccw:0.557522;228,223,175,255;rgb;ccw:0.734513;230,202,148,255;rgb;ccw:0.823009;205,171,131,255;rgb;ccw:0.911504;181,152,128,255;rgb;ccw" k="stops"/>
          </colorramp>
          <item label="-2" value="-1.5" color="#001e50" alpha="255"/>
          <item label="-1" value="-1.3" color="#003366" alpha="255"/>
          <item label="-1" value="-1.1" color="#006699" alpha="255"/>
          <item label="-1" value="-0.9" color="#0099cd" alpha="255"/>
          <item label="-1" value="-0.6" color="#64c8ff" alpha="255"/>
          <item label="-0" value="-0.3" color="#c6ecff" alpha="255"/>
          <item label="0" value="0" color="#94ab84" alpha="255"/>
          <item label="10" value="10" color="#acbf8b" alpha="255"/>
          <item label="20" value="20" color="#bdcc96" alpha="255"/>
          <item label="30" value="30" color="#e4dfaf" alpha="255"/>
          <item label="40" value="40" color="#e6ca94" alpha="255"/>
          <item label="45" value="45" color="#cdab83" alpha="255"/>
          <item label="50" value="50" color="#b59880" alpha="255"/>
          <item label="55" value="55" color="#9b7b62" alpha="255"/>
          <rampLegendSettings useContinuousLegend="1" orientation="2" direction="0" prefix="" minimumLabel="" maximumLabel="" suffix="">
            <numericFormat id="basic">
              <Option type="Map">
                <Option value="" name="decimal_separator" type="QChar"/>
                <Option value="6" name="decimals" type="int"/>
                <Option value="0" name="rounding_type" type="int"/>
                <Option value="false" name="show_plus" type="bool"/>
                <Option value="true" name="show_thousand_separator" type="bool"/>
                <Option value="false" name="show_trailing_zeros" type="bool"/>
                <Option value="" name="thousand_separator" type="QChar"/>
              </Option>
            </numericFormat>
          </rampLegendSettings>
        </colorrampshader>
      </rastershader>
    </rasterrenderer>
    <brightnesscontrast contrast="0" gamma="1" brightness="-100"/>
    <huesaturation colorizeOn="0" saturation="50" grayscaleMode="0" colorizeRed="255" colorizeGreen="128" colorizeBlue="128" colorizeStrength="100" invertColors="0"/>
    <rasterresampler zoomedOutResampler="cubic" zoomedInResampler="cubic" maxOversampling="2"/>
    <resamplingStage>resamplingFilter</resamplingStage>
  </pipe>
  <blendMode>8</blendMode>
</qgis>
