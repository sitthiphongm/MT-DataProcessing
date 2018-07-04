#!/bin/bash
TO_ENCODING="UTF-8"
for entry in $(pwd)/*.${1}
do
	if [ "$1" = 'th' ]; then 
	    FROM_ENCODING="TIS-620"
	else
		FROM_ENCODING=$(file -i $entry)
		FROM_ENCODING=$(echo $FROM_ENCODING | awk -F '=' '{print $2}')
	fi

	# echo $FROM_ENCODING
	CONVERT=" iconv  -f   $FROM_ENCODING  -t   $TO_ENCODING"
	
	if [[ -z "$2" ]]; then
		$CONVERT   "$entry"   -o  "${entry%.txt}.utf8.converted"
	else
		filename=$(echo $entry | awk '{n=split($0, array, "/")} END{print n }')
		filename=$(echo $entry | cut -d '/' -f $filename)
		# echo "$2/${entry%.txt}.utf8.converted"
		$CONVERT   "$entry"   -o  "$2/${filename}"
	fi	
done