def calculate_ssc_marks(url, pos_mark, neg_mark):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }
    try:
        # 1. URL fetch karo
        res = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # 2. Universal Search: Ab hum kisi specific class par depend nahi karenge
        # Hum saari tables dhundenge aur check karenge ki kis table mein "Right Answer" likha hai
        blocks = soup.find_all('table') 
        
        correct, wrong, blank = 0, 0, 0
        question_data = []

        for table in blocks:
            # Check if this table contains a question
            if "Right Answer" in table.text and "Chosen Option" in table.text:
                
                # Right Answer nikalna
                right_ans = ""
                rows = table.find_all('tr')
                for row in rows:
                    if "Right Answer" in row.text:
                        # Right answer usually ek specific td mein hota hai
                        right_ans = row.find_all('td')[1].text.strip().split('.')[0]
                
                # Chosen Option nikalna
                chosen_ans = "--"
                for row in rows:
                    if "Chosen Option" in row.text:
                        chosen_ans = row.find_all('td')[1].text.strip()
                        break
                
                # Compare
                if chosen_ans == "--":
                    blank += 1
                    question_data.append("Blank")
                elif chosen_ans == right_ans:
                    correct += 1
                    question_data.append("Correct")
                else:
                    wrong += 1
                    question_data.append("Wrong")
        
        # Agar koi bhi question nahi mila
        if len(question_data) == 0:
            return None, "No questions found! SSC ne site ka layout change kar diya hai."

        score = (correct * pos_mark) - (wrong * neg_mark)
        return (correct, wrong, blank, round(score, 2), question_data), "Success"
        
    except Exception as e:
        return None, str(e)
