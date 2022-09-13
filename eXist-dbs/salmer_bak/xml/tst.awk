BEGIN { print "["}
/<pb[^>]+>/{
  sub(/rend="="[ ]+/, "")
  match($0, /n="[^"]+"/)
  print "\t{"
  print "\t\t\"name\" : "substr($0,RSTART+2,RLENGTH-2)","
  match($0, /facs="[^"]+"/)
  print "\t\t\"file\" : "substr($0,RSTART+5,RLENGTH-6)".jpg\""
  print "\t},"}
END { print "]" }
