<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:junos="http://xml.juniper.net/junos/*/junos"
    xmlns:xnm="http://xml.juniper.net/xnm/1.1/xnm" xmlns:ext="http://xmlsoft.org/XSLT/namespace"
    xmlns:jcs="http://xml.juniper.net/junos/commit-scripts/1.0">
    
    <xsl:variable name="connection" select="jcs:open()"/> 
    
    <xsl:template match="/">
        <op-script-results>
            <xsl:variable name="rpc-command">
                <rpc>
                    <get-zones-information>
                    </get-zones-information>
                </rpc>
            </xsl:variable>
            <output>
                <xsl:value-of select="jcs:execute($connection,$rpc-command)"/>
            </output>
        </op-script-results>    
    </xsl:template>
</xsl:stylesheet>