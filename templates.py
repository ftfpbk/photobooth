# dictionary to store templates for composite images, basically sizes, locations, and temp file names
templates = {'display':[ ['504x336', '+12+12', 'images/backscreen-hd.jpg', 'boutput.jpg'],
			['504x336', '+12+373', 'boutput.jpg', 'boutput.jpg'],
			['504x336', '+540+12', 'boutput.jpg', 'boutput.jpg'],
			['504x336', '+540+373', 'boutput.jpg', 'boutput.jpg'],
			['+411+243', 'x233', 'images/overlay-disp.png', 'boutput.jpg'], 
			'gm composite -resize &ARG1 -geometry &ARG2 &FILENAME_&I.jpg &ARG3 -quality 98 &ARG4 ',
			'gm composite -geometry &ARG1 -resize &ARG2 &ARG3 &ARG4 -quality 95 &FILENAME_&TEMPLATE.jpg '
			],

	      'phone':[ ['1756x1164', '+120+996', 'images/background-half-big.jpg', 'output.jpg'],
			['1756x1164', '+120+2248', 'output.jpg', 'output.jpg'],
			['1756x1164', '+120+3500', 'output.jpg', 'output.jpg'],
			['1756x1164', '+120+4752', 'output.jpg', 'output.jpg'],
			['+250+50', '1500x', 'images/overlay-phone.png', 'output.jpg'], 
			'gm composite -resize &ARG1 -geometry &ARG2 &FILENAME_&I.jpg &ARG3 -quality 98 &ARG4 ',
			'gm composite -geometry &ARG1 -resize &ARG2 &ARG3 &ARG4 -quality 95 &FILENAME_&TEMPLATE.jpg '
			],

	'display-4x6':[ ['504x336', '+12+12', 'images/backscreen-hd.jpg', 'boutput.jpg'],
			['504x336', '+12+373', 'boutput.jpg', 'boutput.jpg'],
			['504x336', '+540+12', 'boutput.jpg', 'boutput.jpg'],
			['504x336', '+540+373', 'boutput.jpg', 'boutput.jpg'],
			['+411+243', 'x233', 'images/overlay-disp.png', 'boutput.jpg'], 
			'gm composite -resize &ARG1 -geometry &ARG2 &FILENAME_&I.jpg &ARG3 -quality 98 &ARG4 ',
			'gm composite -geometry &ARG1 -resize &ARG2 &ARG3 &ARG4 -quality 95 &FILENAME_&TEMPLATE.jpg '
			],


	  'phone-4x6':[ ['1756x1164', '+1120+996', 'images/background-big.jpg', 'output.jpg'],
			['1756x1164', '+1120+2248', 'output.jpg', 'output.jpg'],
			['1756x1164', '+1120+3500', 'output.jpg', 'output.jpg'],
			['1756x1164', '+1120+4752', 'output.jpg', 'output.jpg'],
			['+1250+50', '1500x', 'images/overlay-phone.png', 'output.jpg'], 
			'gm composite -resize &ARG1 -geometry &ARG2 &FILENAME_&I.jpg &ARG3 -quality 98 &ARG4 ',
			'gm composite -geometry &ARG1 -resize &ARG2 &ARG3 &ARG4 -quality 95 &FILENAME_&TEMPLATE.jpg '
			],

	'display-1x3':[ ['504x336', '+12+12', 'images/backscreen-hd.jpg', 'boutput.jpg'],
			['504x336', '+12+373', 'boutput.jpg', 'boutput.jpg'],
			['504x336', '+540+12', 'boutput.jpg', 'boutput.jpg'],
			['504x336', '+540+373', 'boutput.jpg', 'boutput.jpg'],
			['+411+243', 'x233', 'images/overlay-disp.png', 'boutput.jpg'], 
			'gm composite -resize &ARG1 -geometry &ARG2 &FILENAME_&I.jpg &ARG3 -quality 98 &ARG4 ',
			'gm convert -font Courier -pointsize 20 -fill black -draw "text 1070,365 &FILENAME" boutput.jpg boutput.jpg; gm composite -geometry &ARG1 -resize &ARG2 &ARG3 &ARG4 -quality 95 &FILENAME_&TEMPLATE.jpg '
			],


	  'phone-1x3':[ ['878x582', '+61+498', 'images/background-big1k3k.jpg', 'output.jpg'],
			['878x582', '+61+1124', 'output.jpg', 'output.jpg'],
			['878x582', '+61+1750', 'output.jpg', 'output.jpg'],
			['878x582', '+61+2376', 'output.jpg', 'output.jpg'],
			['+125+25', '750x', 'images/overlay-phone.png', 'output.jpg'], 
			'gm composite -resize &ARG1 -geometry &ARG2 &FILENAME_&I.jpg &ARG3 -quality 98 &ARG4 ',
			'gm convert -font Courier -pointsize 30 -fill black -draw "text 61,485 &FILENAME" output.jpg output.jpg; gm composite -geometry &ARG1 -resize &ARG2 &ARG3 &ARG4 -quality 95 &FILENAME_&TEMPLATE.jpg '
			],

	'display-2x3':[ ['504x336', '+12+12', 'images/backscreen-hd.jpg', 'boutput.jpg'],
			['504x336', '+12+373', 'boutput.jpg', 'boutput.jpg'],
			['504x336', '+540+12', 'boutput.jpg', 'boutput.jpg'],
			['504x336', '+540+373', 'boutput.jpg', 'boutput.jpg'],
			['+411+243', 'x233', 'images/overlay-disp.png', 'boutput.jpg'], 
			'gm composite -resize &ARG1 -geometry &ARG2 &FILENAME_&I.jpg &ARG3 -quality 98 &ARG4 ',
			'gm composite -geometry &ARG1 -resize &ARG2 &ARG3 &ARG4 -quality 95 &FILENAME_&TEMPLATE.jpg '
			],


	  'phone-2x3':[ ['878x582', '+560+498', 'images/background-big2k3k.jpg', 'output.jpg'],
			['878x582', '+560+1124', 'output.jpg', 'output.jpg'],
			['878x582', '+560+1750', 'output.jpg', 'output.jpg'],
			['878x582', '+560+2376', 'output.jpg', 'output.jpg'],
			['+625+25', '750x', 'images/overlay-phone.png', 'output.jpg'], 
			'gm composite -resize &ARG1 -geometry &ARG2 &FILENAME_&I.jpg &ARG3 -quality 98 &ARG4 ',
			'gm composite -geometry &ARG1 -resize &ARG2 &ARG3 &ARG4 -quality 95 &FILENAME_&TEMPLATE.jpg '
			],

	    'display-sepia':[ ['504x336', '+12+12', 'images/backscreen-hd.jpg', 'boutput.jpg'],
			['504x336', '+12+373', 'boutput.jpg', 'boutput.jpg'],
			['504x336', '+540+12', 'boutput.jpg', 'boutput.jpg'],
			['504x336', '+540+373', 'boutput.jpg', 'boutput.jpg'],
			['+411+243', 'x233', 'images/overlay-disp.png', 'boutput.jpg'], 
			'gm convert -resize &ARG1 &FILENAME_&I.jpg -modulate 115,0,100 -colorize 7,21,50 coloroutput.jpg; gm composite -geometry &ARG2 coloroutput.jpg &ARG3 -quality 98 &ARG4 ',
			'gm composite -geometry &ARG1 -resize &ARG2 &ARG3 &ARG4 -quality 95 &FILENAME_&TEMPLATE.jpg '
			],

	'phone-sepia':[ ['1756x1164', '+120+996', 'images/background-half-big.jpg', 'output.jpg'],
			['1756x1164', '+120+2248', 'output.jpg', 'output.jpg'],
			['1756x1164', '+120+3500', 'output.jpg', 'output.jpg'],
			['1756x1164', '+120+4752', 'output.jpg', 'output.jpg'],
			['+250+50', '1500x', 'images/overlay-phone.png', 'output.jpg'], 
			'gm convert -resize &ARG1 &FILENAME_&I.jpg -modulate 115,0,100 -colorize 7,21,50 coloroutput.jpg; gm composite -geometry &ARG2 coloroutput.jpg &ARG3 -quality 98 &ARG4 ',
			'gm composite -geometry &ARG1 -resize &ARG2 &ARG3 &ARG4 -quality 95 &FILENAME_&TEMPLATE.jpg '
			],

	 'display-bw':[ ['504x336', '+12+12', 'images/backscreen-hd.jpg', 'boutput.jpg'],
			['504x336', '+12+373', 'boutput.jpg', 'boutput.jpg'],
			['504x336', '+540+12', 'boutput.jpg', 'boutput.jpg'],
			['504x336', '+540+373', 'boutput.jpg', 'boutput.jpg'],
			['+411+243', 'x233', 'images/overlay-disp.png', 'boutput.jpg'], 
			'gm convert -resize &ARG1 &FILENAME_&I.jpg -colorspace GRAY coloroutput.jpg; gm composite -geometry &ARG2 coloroutput.jpg &ARG3 -quality 98 &ARG4 ',
			'gm composite -geometry &ARG1 -resize &ARG2 &ARG3 &ARG4 -quality 95 &FILENAME_&TEMPLATE.jpg '
			],

	   'phone-bw':[ ['1756x1164', '+120+996', 'images/background-half-big.jpg', 'output.jpg'],
			['1756x1164', '+120+2248', 'output.jpg', 'output.jpg'],
			['1756x1164', '+120+3500', 'output.jpg', 'output.jpg'],
			['1756x1164', '+120+4752', 'output.jpg', 'output.jpg'],
			['+250+50', '1500x', 'images/overlay-phone.png', 'output.jpg'], 
			'gm convert -resize &ARG1 &FILENAME_&I.jpg -colorspace GRAY coloroutput.jpg; gm composite -geometry &ARG2 coloroutput.jpg &ARG3 -quality 98 &ARG4 ',
			'gm composite -geometry &ARG1 -resize &ARG2 &ARG3 &ARG4 -quality 95 &FILENAME_&TEMPLATE.jpg '
			]
		}

