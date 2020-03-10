# Therapy-bot
Länk till kod som använts för att skapa modell: https://colab.research.google.com/drive/1SOVwda_sT_VyIFJkAecwn2MK8222hn6Y 

## Therapy-Bot:

Therapy bot är en bot som skapades för att kunna svara på meddelanden som en terapeut. Den anpassar sina svar någolunda till användarens meddelande och svarar på en kommentar var femte minut så länge kommentaren har placerats i kommentarsfältet till en post på subredditen https://www.reddit.com/r/therapybot/. Therapy-Bot lägger även upp en post varje 24:e timme för att man ska kunna ha flera ställen att kommentera i så att inte en post blir överfull. 

## Hur gjordes Therapy-Bot?:

Therapy bot började som en samling av samtal mellan terapeuter och andra människor. Allt terapeuterna sade placerades i filen therapist_conversations.txt. Denna text användes senare till att skapa en textgenererande modell med hjälp av Natrual Language Processing genom GPT-2 (hittas i länken till google colab). Den använder sig av en text för att generera en ny som liknar den tidigare utan att kopiera exakt. Denna modell läggs sedan upp på google drive för att kunna hämtas ned och kommas åt utan att behöva ha på datorn. Detta möjliggör att Therapy-Bot kan köras från en annan tjänst som t.ex. Heroku. 

Själva scriptet som kör Therapy-Bot hämtar ned denna fil och packar upp den. Det hämtar även ned ett antal ID:s för kommentarer, sparade på en databas så att den inte kan svara på samma kommentar mer än en gång. För denna databas används AWS:s DynamoDB, Lambda och APIGateway. En Lambda funktion skapades för att hämta alla ID:s från databasen och en för att lägga upp ett nytt. Därefter skapades en APIGateway för att kunna kalla dessa funktioner med hjälp av API-requests.  

Botten använder sig sedan av modellen för att generera text med användarens kommentar som prefix. Därefter tas den första meningen innehållande prefixen och den sista meningen som saknar avslutning bort så att meddelanden fungerar grammatiskt och inte repeterar det som användaren sagt. För att kunna svara på användarens kommentar behövs en bot ansluten med reddit. För att göra en sådan förljde jag denna guide: https://www.pythonforengineers.com/build-a-reddit-bot-part-1/

Botten hämtar ned alla posts på subredditen och svarar på den första kommentaren som inte redan finns på databasen som finns. Därefter lägger den till ID:t på den kommentaren i databasen och väntar fem minuter innan den försöker svara på en ny kommentar. Detta därför att reddit inte tillåter allt för många anrop från en bot och koden krashar. 

## Reflektion:

I nuläget har botten ett antal svagheter och förbättringsmöjligheter. För det första ligger scriptet inte uppe på någon hosting service eller liknande. Den måste i nuläget köras från den egna datorn och fungerar inte utan internet. Detta är en sak som skulle kunna förbättras med lite mer tid och ett antal fler försök och man skulle som sagt kunna använda sig av Heroku. Ännu en sak som kan förbätras är bottens förmåga att svara på ett sätt som hänger ihop med användarens kommentar. I nuläget så är det enda som håller ihop kommentaren och svaret att den mening som kommer innan svaret innehåller kommentaren. Detta, i kombination med att texten bara är baserad på svar på en fråga utan att veta vad frågan är gör att botten inte blir så träffsäker i sina svar. Detta skulle man kunna lösa genom att använda ett annat textgenereringsformat som är skapat specifikt för att svara på frågor.

## Vad har jag lärt mig: 

Jag har under projektets gång lärt mig mycket om hur man kommunicerar med reddit med hjälp av PRAW samt hur man hanterar och manipulerar data som man får ut ifrån GPT-2:s textgeneration. 


