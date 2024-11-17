import asyncio
from asyncua import Client, ua
import numpy as np
import cv2
import numpy as np

"""async def write_data(value_write):
    url = "opc.tcp://localhost:4840/"
    async with Client(url=url) as client:
        #objects = client.get_objects_node()
        #print("Objects node is: ", objects)

        var = client.get_node("ns=2;i=2")
        
        dv_value_write = ua.DataValue(ua.Variant(value_write,ua.VariantType.Int16))
        await var.write_value(dv_value_write)
        print(f"\nValue write: {dv_value_write}\n")"""

async def write_data(segment, color):
    url = "opc.tcp://192.168.0.26:4840/"  # OPCUA Server address & port no.
    async with Client(url=url) as client:
        light_segment = client.get_node("ns=4;s=MAIN.lightSegment")  # Corrected NodeID
        workpiece_color = client.get_node("ns=4;s=MAIN.workpieceColor")  # Corrected NodeID
        dv_segment = ua.DataValue(ua.Variant(segment, ua.VariantType.Int16))  # Data type
        dv_color = ua.DataValue(ua.Variant(color, ua.VariantType.Int16))  # Data type
        await workpiece_color.set_value(dv_color)
        await light_segment.set_value(dv_segment)

"""async def read_data():
    url = "opc.tcp://localhost:4840/"
    async with Client(url=url) as client:
        #objects = client.get_objects_node()
        #print("Objects node is: ", objects)

        var = client.get_node("ns=2;i=2")
        
        value_read = await var.read_value()
        print(f"\nValue read: {value_read}\n")"""

def main():
    action = 9
    while action != 0:
        print("Please select:")
        print(" 1. Sorting Process Start")
        print(" 2. Sorting Process Stop")
        print(" 0 Exit")
        action = int(input("Select: "))

        if action == 1:
            
                #segment = int(input("Segment number: "))
                #color = int(input("Color number: "))
                #segment = np.random.randint(1,6,size = 5)
                #color = np.random.randint(1,6,size =5 )
                #for segment1,color1 in zip(segment,color):
                    #asyncio.run(write_data(segment1, color1))
                    pass
                    
               
        elif action == 2:
            value_write = int(input("Please enter number to write: "))
            asyncio.run(write_data(value_write, value_write))  # Corrected to pass both segment and color
        elif action == 0:
            print("Exiting...")
        else:
            print("Invalid selection. Please try again.")



#Detecing Colors


cap = cv2.VideoCapture(0)

while True:
    segment = int(np.random.randint(1,6,size = 1))
    
    ret, frame = cap.read()
    if not ret:
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Green Color Detection
    lower_green = np.array([45, 100, 100])
    upper_green = np.array([75, 255, 255])
    green_mask = cv2.inRange(hsv, lower_green, upper_green)
    res_green = cv2.bitwise_and(frame, frame, mask=green_mask)
    green_contours, _ = cv2.findContours(green_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for contour in green_contours:
        area = cv2.contourArea(contour)
        if area > 3000:
            asyncio.run(write_data(segment,1))
            x, y, w, h = cv2.boundingRect(contour)
            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, "Green Colour", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Red Color Detection
    lower_red1 = np.array([0, 100, 100])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([160, 100, 100])
    upper_red2 = np.array([180, 255, 255])
    red_mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    red_mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    red_mask = red_mask1 | red_mask2
    res_red = cv2.bitwise_and(frame, frame, mask=red_mask)
    red_contours, _ = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for contour in red_contours:
        area = cv2.contourArea(contour)
        if area > 5000:
            asyncio.run(write_data(segment,2))
            x, y, w, h = cv2.boundingRect(contour)
            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(frame, "Red Colour", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

    # Yellow Color Detection
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([30, 255, 255])
    yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    res_yellow = cv2.bitwise_and(frame, frame, mask=yellow_mask)
    yellow_contours, _ = cv2.findContours(yellow_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for contour in yellow_contours:
        area = cv2.contourArea(contour)
        if area > 5000:
            asyncio.run(write_data(segment,3))
            x, y, w, h = cv2.boundingRect(contour)
            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
            cv2.putText(frame, "Yellow Colour", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)

    # Blue Color Detection
    lower_blue = np.array([94, 80, 2])
    upper_blue = np.array([126, 255, 255])
    blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)
    res_blue = cv2.bitwise_and(frame, frame, mask=blue_mask)
    blue_contours, _ = cv2.findContours(blue_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for contour in blue_contours:
        area = cv2.contourArea(contour)
        if area > 3000:
            asyncio.run(write_data(segment,4))
            x, y, w, h = cv2.boundingRect(contour)
            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(frame, "Blue Colour", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

    # Orange Color Detection
    lower_orange = np.array([10, 100, 20])
    upper_orange = np.array([25, 255, 255])
    orange_mask = cv2.inRange(hsv, lower_orange, upper_orange)
    res_orange = cv2.bitwise_and(frame, frame, mask=orange_mask)
    orange_contours, _ = cv2.findContours(orange_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for contour in orange_contours:
        area = cv2.contourArea(contour)
        if area > 5000:
            asyncio.run(write_data(segment, 5))
            x, y, w, h = cv2.boundingRect(contour)
            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 165, 255), 2)
            cv2.putText(frame, "Orange Colour", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 165, 255), 2)
   # Define colors dictionary
    #colors = {1: (0, 255, 0), 2: (0, 0, 255), 3: (0, 255, 255), 4: (255, 0, 0), 5: (0, 165, 255)}



# Generate a random color key
    #random_color_key = np.random.randint(1, 6)

# Get the color from the dictionary based on the random key
    #random_color = colors[random_color_key]

# Draw circles with the random color
    cv2.circle(frame, (50, 50), 20, (0,255,0), 2)
    cv2.circle(frame, (100, 50), 20, (0,255,0), 2)
    cv2.circle(frame, (150, 50), 20, (0,255,0), 2)
    cv2.circle(frame, (200, 50), 20, (0,255,0), 2)
    cv2.circle(frame, (250, 50), 20, (0,255,0), 2)

    

    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()









if __name__ == "__main__":
    main()
    
    
    
    

