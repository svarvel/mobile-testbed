#!/usr/bin/env python
import sys
import xml.etree.ElementTree as ET

def main(s):
    names=list()
    selected=list()
    foundTests=0
    tree = ET.parse("window_dump.xml")
    root = tree.getroot()
    for child in root.iter():
        if child.attrib.get("resource-id") == "mobi.meddle.wehe:id/app_name_textview": 
            names.append(child.attrib.get("text"))
        elif child.attrib.get("resource-id") == "mobi.meddle.wehe:id/isSelectedSwitch":
            isSelected = child.attrib.get("checked")
            if isSelected == "false":
                print(child.attrib.get("bounds").replace("[","").split("]")[0].replace(",", " "))
            selected.append(child.attrib.get("checked")) 
            foundTests+=1
    print(foundTests)
    # print(names[:len(selected)])
    # print(selected)


if '__main__' == __name__:
    s="""<?xml version='1.0' encoding='UTF-8' standalone='yes' ?><hierarchy rotation="0"><node index="0" text="" resource-id="" class="android.widget.FrameLayout" package="mobi.meddle.wehe" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[0,0][1080,2190]"><node index="0" text="" resource-id="" class="android.widget.LinearLayout" package="mobi.meddle.wehe" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[0,0][1080,2190]"><node index="0" text="" resource-id="" class="android.widget.FrameLayout" package="mobi.meddle.wehe" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[0,0][1080,2190]"><node index="0" text="" resource-id="mobi.meddle.wehe:id/action_bar_root" class="android.widget.LinearLayout" package="mobi.meddle.wehe" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[0,0][1080,2190]"><node index="0" text="" resource-id="android:id/content" class="android.widget.FrameLayout" package="mobi.meddle.wehe" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[0,0][1080,2190]"><node index="0" text="" resource-id="mobi.meddle.wehe:id/drawer_layout" class="androidx.drawerlayout.widget.DrawerLayout" package="mobi.meddle.wehe" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[0,0][1080,2190]"><node index="0" text="" resource-id="" class="android.widget.LinearLayout" package="mobi.meddle.wehe" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[0,75][1080,2190]"><node index="0" text="" resource-id="mobi.meddle.wehe:id/main_app_bar" class="android.view.ViewGroup" package="mobi.meddle.wehe" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[0,75][1080,233]"><node index="0" text="" resource-id="" class="android.widget.ImageButton" package="mobi.meddle.wehe" content-desc="Open navigation drawer" checkable="false" checked="false" clickable="true" enabled="true" focusable="true" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[0,75][158,233]" /><node index="1" text="Differentiation Tests" resource-id="" class="android.widget.TextView" package="mobi.meddle.wehe" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[202,116][715,192]" /></node><node index="1" text="" resource-id="mobi.meddle.wehe:id/content_frame" class="android.widget.FrameLayout" package="mobi.meddle.wehe" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[0,233][1080,2190]"><node index="0" text="" resource-id="mobi.meddle.wehe:id/selection_layout" class="android.widget.RelativeLayout" package="mobi.meddle.wehe" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[0,233][1080,2190]"><node index="0" text="" resource-id="mobi.meddle.wehe:id/appsRecyclerView" class="androidx.recyclerview.widget.RecyclerView" package="mobi.meddle.wehe" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="true" focused="false" scrollable="true" long-clickable="false" password="false" selected="false" bounds="[0,233][1080,1925]"><node index="0" text="" resource-id="" class="android.widget.LinearLayout" package="mobi.meddle.wehe" content-desc="" checkable="false" checked="false" clickable="true" enabled="true" focusable="true" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[0,233][1080,548]"><node index="0" text="" resource-id="mobi.meddle.wehe:id/cv" class="android.widget.FrameLayout" package="mobi.meddle.wehe" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[45,278][1035,503]"><node index="0" text="" resource-id="" class="android.widget.RelativeLayout" package="mobi.meddle.wehe" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[45,278][1035,503]"><node index="0" text="" resource-id="mobi.meddle.wehe:id/appImageView" class="android.widget.ImageView" package="mobi.meddle.wehe" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[45,278][270,503]" /><node index="1" text="Disney+" resource-id="mobi.meddle.wehe:id/app_name_textview" class="android.widget.TextView" package="mobi.meddle.wehe" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[315,278][454,331]" /><node index="2" text="Time: 8 seconds" resource-id="mobi.meddle.wehe:id/app_time_textview" class="android.widget.TextView" package="mobi.meddle.wehe" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[315,354][600,407]" /><node index="3" text="" resource-id="mobi.meddle.wehe:id/isSelectedSwitch" class="android.widget.Switch" package="mobi.meddle.wehe" content-desc="" checkable="true" checked="false" clickable="false" enabled="true" focusable="true" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[903,352][1035,428]" /><node index="4" text="Size: 2 x 16 MB" resource-id="mobi.meddle.wehe:id/app_size_textview" class="android.widget.TextView" package="mobi.meddle.wehe" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[315,430][579,483]" /></node></node></node><node index="1" text="" resource-id="" class="android.widget.LinearLayout" package="mobi.meddle.wehe" content-desc="" checkable="false" checked="false" clickable="true" enabled="true" focusable="true" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[0,548][1080,863]"><node index="0" text="" resource-id="mobi.meddle.wehe:id/cv" class="android.widget.FrameLayout" package="mobi.meddle.wehe" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[45,593][1035,818]"><node index="0" text="" resource-id="" class="android.widget.RelativeLayout" package="mobi.meddle.wehe" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[45,593][1035,818]"><node index="0" text="" resource-id="mobi.meddle.wehe:id/appImageView" class="android.widget.ImageView" package="mobi.meddle.wehe" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[45,593][270,818]" /><node index="1" text="Facebook Video" resource-id="mobi.meddle.wehe:id/app_name_textview" class="android.widget.TextView" package="mobi.meddle.wehe" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[315,593][595,646]" /><node index="2" text="Time: 46 seconds" resource-id="mobi.meddle.wehe:id/app_time_textview" class="android.widget.TextView" package="mobi.meddle.wehe" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[315,669][622,722]" /><node index="3" text="" resource-id="mobi.meddle.wehe:id/isSelectedSwitch" class="android.widget.Switch" package="mobi.meddle.wehe" content-desc="" checkable="true" checked="true" clickable="false" enabled="true" focusable="true" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[903,667][1035,743]" /><node index="4" text="Size: 2 x 14 MB" resource-id="mobi.meddle.wehe:id/app_size_textview" class="android.widget.TextView" package="mobi.meddle.wehe" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[315,745][579,798]" /></node></node></node><node index="2" text="" resource-id="" class="android.widget.LinearLayout" package="mobi.meddle.wehe" content-desc="" checkable="false" checked="false" clickable="true" enabled="true" focusable="true" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[0,863][1080,1178]"><node index="0" text="" resource-id="mobi.meddle.wehe:id/cv" class="android.widget.FrameLayout" package="mobi.meddle.wehe" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[45,908][1035,1133]"><node index="0" text="" resource-id="" class="android.widget.RelativeLayout" package="mobi.meddle.wehe" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[45,908][1035,1133]"><node index="0" text="" resource-id="mobi.meddle.wehe:id/appImageView" class="android.widget.ImageView" package="mobi.meddle.wehe" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[45,908][270,1133]" /><node index="1" text="Hulu" resource-id="mobi.meddle.wehe:id/app_name_textview" class="android.widget.TextView" package="mobi.meddle.wehe" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[315,908][397,961]" /><node index="2" text="Time: 32 seconds" resource-id="mobi.meddle.wehe:id/app_time_textview" class="android.widget.TextView" package="mobi.meddle.wehe" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[315,984][622,1037]" /><node index="3" text="" resource-id="mobi.meddle.wehe:id/isSelectedSwitch" class="android.widget.Switch" package="mobi.meddle.wehe" content-desc="" checkable="true" checked="false" clickable="false" enabled="true" focusable="true" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[903,982][1035,1058]" /><node index="4" text="Size: 2 x 14 MB" resource-id="mobi.meddle.wehe:id/app_size_textview" class="android.widget.TextView" package="mobi.meddle.wehe" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[315,1060][579,1113]" /></node></node></node><node index="3" text="" resource-id="" class="android.widget.LinearLayout" package="mobi.meddle.wehe" content-desc="" checkable="false" checked="false" clickable="true" enabled="true" focusable="true" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[0,1178][1080,1493]"><node index="0" text="" resource-id="mobi.meddle.wehe:id/cv" class="android.widget.FrameLayout" package="mobi.meddle.wehe" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[45,1223][1035,1448]"><node index="0" text="" resource-id="" class="android.widget.RelativeLayout" package="mobi.meddle.wehe" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[45,1223][1035,1448]"><node index="0" text="" resource-id="mobi.meddle.wehe:id/appImageView" class="android.widget.ImageView" package="mobi.meddle.wehe" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[45,1223][270,1448]" /><node index="1" text="NBC Sports" resource-id="mobi.meddle.wehe:id/app_name_textview" class="android.widget.TextView" package="mobi.meddle.wehe" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[315,1223][520,1276]" /><node index="2" text="Time: 48 seconds" resource-id="mobi.meddle.wehe:id/app_time_textview" class="android.widget.TextView" package="mobi.meddle.wehe" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[315,1299][622,1352]" /><node index="3" text="" resource-id="mobi.meddle.wehe:id/isSelectedSwitch" class="android.widget.Switch" package="mobi.meddle.wehe" content-desc="" checkable="true" checked="false" clickable="false" enabled="true" focusable="true" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[903,1297][1035,1373]" /><node index="4" text="Size: 2 x 19 MB" resource-id="mobi.meddle.wehe:id/app_size_textview" class="android.widget.TextView" package="mobi.meddle.wehe" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[315,1375][579,1428]" /></node></node></node><node index="4" text="" resource-id="" class="android.widget.LinearLayout" package="mobi.meddle.wehe" content-desc="" checkable="false" checked="false" clickable="true" enabled="true" focusable="true" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[0,1493][1080,1808]"><node index="0" text="" resource-id="mobi.meddle.wehe:id/cv" class="android.widget.FrameLayout" package="mobi.meddle.wehe" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[45,1538][1035,1763]"><node index="0" text="" resource-id="" class="android.widget.RelativeLayout" package="mobi.meddle.wehe" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[45,1538][1035,1763]"><node index="0" text="" resource-id="mobi.meddle.wehe:id/appImageView" class="android.widget.ImageView" package="mobi.meddle.wehe" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[45,1538][270,1763]" /><node index="1" text="Netflix" resource-id="mobi.meddle.wehe:id/app_name_textview" class="android.widget.TextView" package="mobi.meddle.wehe" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[315,1538][431,1591]" /><node index="2" text="Time: 60 seconds" resource-id="mobi.meddle.wehe:id/app_time_textview" class="android.widget.TextView" package="mobi.meddle.wehe" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[315,1614][622,1667]" /><node index="3" text="" resource-id="mobi.meddle.wehe:id/isSelectedSwitch" class="android.widget.Switch" package="mobi.meddle.wehe" content-desc="" checkable="true" checked="false" clickable="false" enabled="true" focusable="true" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[903,1612][1035,1688]" /><node index="4" text="Size: 2 x 15 MB" resource-id="mobi.meddle.wehe:id/app_size_textview" class="android.widget.TextView" package="mobi.meddle.wehe" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[315,1690][579,1743]" /></node></node></node><node index="5" text="" resource-id="" class="android.widget.LinearLayout" package="mobi.meddle.wehe" content-desc="" checkable="false" checked="false" clickable="true" enabled="true" focusable="true" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[0,1808][1080,1925]"><node index="0" text="" resource-id="mobi.meddle.wehe:id/cv" class="android.widget.FrameLayout" package="mobi.meddle.wehe" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[45,1853][1035,1925]"><node index="0" text="" resource-id="" class="android.widget.RelativeLayout" package="mobi.meddle.wehe" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[45,1853][1035,1925]"><node index="0" text="" resource-id="mobi.meddle.wehe:id/appImageView" class="android.widget.ImageView" package="mobi.meddle.wehe" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[45,1853][270,1925]" /><node index="1" text="Prime Video" resource-id="mobi.meddle.wehe:id/app_name_textview" class="android.widget.TextView" package="mobi.meddle.wehe" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[315,1853][529,1906]" /></node></node></node></node><node index="1" text="" resource-id="mobi.meddle.wehe:id/appTabs" class="android.widget.LinearLayout" package="mobi.meddle.wehe" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[0,1925][1080,2077]"><node index="0" text="Video" resource-id="mobi.meddle.wehe:id/videoButton" class="android.widget.Button" package="mobi.meddle.wehe" content-desc="" checkable="false" checked="false" clickable="true" enabled="true" focusable="true" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[0,1925][339,2077]" /><node index="1" text="Music" resource-id="mobi.meddle.wehe:id/musicButton" class="android.widget.Button" package="mobi.meddle.wehe" content-desc="" checkable="false" checked="false" clickable="true" enabled="true" focusable="true" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[342,1925][682,2077]" /><node index="2" text="Conferencing" resource-id="mobi.meddle.wehe:id/conferencingButton" class="android.widget.Button" package="mobi.meddle.wehe" content-desc="" checkable="false" checked="false" clickable="true" enabled="true" focusable="true" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[685,1925][1080,2077]" /></node><node index="2" text="Total size: 70 MB" resource-id="mobi.meddle.wehe:id/totSizeTextView" class="android.widget.TextView" package="mobi.meddle.wehe" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[0,2077][1080,2130]" /><node index="3" text="DIFFERENTIATION TESTS" resource-id="mobi.meddle.wehe:id/nextButton" class="android.widget.Button" package="mobi.meddle.wehe" content-desc="" checkable="false" checked="false" clickable="true" enabled="true" focusable="true" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[0,2130][1080,2190]" /></node></node></node></node></node></node></node></node><node index="1" text="" resource-id="android:id/statusBarBackground" class="android.view.View" package="mobi.meddle.wehe" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[0,0][1080,75]" /><node index="2" text="" resource-id="android:id/navigationBarBackground" class="android.view.View" package="mobi.meddle.wehe" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[0,0][0,0]" /></node></hierarchy>"""
    # main(sys.argv[1])
    main(s)
