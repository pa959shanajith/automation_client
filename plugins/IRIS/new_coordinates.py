import math
import logger


def getting_new_coor(cord1,cord2):

    # logger.print_on_console(cord1)
    # logger.print_on_console(cord2)
 


    theta_hypo=[]
    # for cord1 in cord_old:
    #     for cord2 in cord_new:
    #if cord1[4]==cord2[5]:
    #print(cord1[4],cord2[0])
    # logger.print_on_console(cord1[0])
    # logger.print_on_console(cord1[1])
    # logger.print_on_console(cord2[2])
    # logger.print_on_console(cord2[3])
    adja=abs(cord1[0]-cord2[0])
    oppo=abs(cord1[1]-cord2[1])
    # logger.print_on_console('opp:',oppo)
    # logger.print_on_console('adja:',adja)
    
    if adja==0 or oppo==0:
        angle=0
        length=0
    else:
        angle=round(math.atan(oppo/adja),2)
    #theta_deg=math.degrees(theta)
        length=round(math.sqrt(pow(adja,2)+pow(oppo,2)),2)

        # logger.print_on_console('angle:',angle)
        # logger.print_on_console('length:',length)

    if (cord1[0]==cord2[0]) or (cord1[1]==cord2[1]):
        length_x=0
        length_y=0

    if cord1[0]>cord2[0]:
        length_x=-length
    else:
        length_x=length

    if cord1[1]>cord2[1]:
        length_y=-length
    else:
        length_y=length
    theta_hypo.append([angle,length_x,length_y])

    #break
            
    theta=theta_hypo[0][0]
    hypo_x=theta_hypo[0][1]
    hypo_y=theta_hypo[0][2]
    return theta,hypo_x,hypo_y
        