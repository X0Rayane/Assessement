from Badge import Badge

#Add many badges as you want
badge_list=[]
badge_list.append(Badge(img_path='image/badge1.png', username="John Doe"))
badge_list.append(Badge(img_path='image/badge2.png'))
badge_list.append(Badge(img_path='image/badge3.png'))
badge_list.append(Badge(img_path='image/badge4.png'))
badge_list.append(Badge(img_path='image/badge5.png'))
badge_list.append(Badge(img_path='image/badge6.png'))
badge_list.append(Badge(img_path='image/badge7.png'))


#A mini shell application to test the code
if __name__ == "__main__":
    init=""
    while init!="quit":
        badge_index=int(input(f"Chose a badge between the {len(badge_list)} existing badge (type a number between 1 and {len(badge_list)}): "))
        valid, message= badge_list[badge_index-1].verify_badge()
        print(message)
        
        while not valid:
            if message in ["Found Non-Transparent pixel outside of the circle","Badge have invalid size (Should be 512x512)"]:
                badge_list[badge_index-1].convert_img()
                valid, message= badge_list[badge_index-1].verify_badge()
                print(message)

            elif message == "Badge contains unhappy colors":
                break

        if valid:    
            badge_list[badge_index-1].get_badge()
        init=input("Type 'quit' or enter to continue : ")
    exit()