def calculate_ssc_marks(url, pos_mark, neg_mark):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }
    try:
        # 1. Fetch the URL content
        res = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(res.text, 'html.parser')

        # 2. Smart Searching Strategy
        # Hum 3 sabse common class names check karenge jo SSC use karta hai.
        question_blocks = soup.find_all('div', class_='question-pnl')      # Style 1
        if not question_blocks:
            question_blocks = soup.find_all('table', class_='menu-tbl')     # Style 2
        if not question_blocks:
            question_blocks = soup.find_all('table', class_='question-tabl') # Style 3
        
        # 3. Final Check: Agar in teeno me se kuch nahi mila
        if not question_blocks:
            return None, "Error: Hum is answer key ka format nahi padh paa rahe hain. Lagta hai SSC ne layout poori tarah badal diya hai."

        # 4. Calculation Engine
        correct, wrong, blank = 0, 0, 0
        question_data = []

        for block in question_blocks:
            # Right Answer (Hamesha 'rightAns' class me hota hai)
            right_ans_elem = block.find('td', class_='rightAns')
            if not right_ans_elem: continue # Agar ye question block nahi hai, toh skip karo
            
            right_ans = right_ans_elem.text.strip()[0]
            
            # Chosen Option
            chosen_ans = "--"
            tds = block.find_all('td')
            for i, td in enumerate(tds):
                if "Chosen Option" in td.text:
                    if i + 1 < len(tds):
                        chosen_ans = tds[i+1].text.strip()
                    break
            
            # Compare
            if chosen_ans in ["--", ""]:
                blank += 1
                question_data.append("Blank")
            elif chosen_ans == right_ans:
                correct += 1
                question_data.append("Correct")
            else:
                wrong += 1
                question_data.append("Wrong")
        
        # Ek aur Safety Check
        if len(question_data) == 0:
            return None, "Error: Lagta hai page load hua par usme questions nahi mile. Link expire ho sakti hai."

        score = (correct * pos_mark) - (wrong * neg_mark)
        return (correct, wrong, blank, round(score, 2), question_data), "Success"
        
    except requests.exceptions.Timeout:
        return None, "Error: SSC server response nahi de raha hai. Thodi der baad try karein."
    except Exception as e:
        return None, f"Technical Error: {e}"
