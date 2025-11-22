# General Thoughts

**139 substantive messages**

---

## 📝 Relevance Questions by Category
**Date**: 2023-08-11 | **Source**: chatgpt

> For these, which
My physical work environment (e.g., office space) allows me to focus on my work
There is plenty of natural light in my workplace
I can conveniently access nature in or close to my work environment (e.g., parks, nature preserves, etc)
My country's political and social climate provides a sense of safety and security
I'm regularly concerned about the negative consequences that the climate crisis will have on my life and the life of loved ones
I feel in control of my digital environment including notifications, social media, and other distractions
I know how to adequately manage my data and privacy online.

---

> I feel secure and supported in both my immediate surroundings and the broader community in which I live
My physical work environment (e.g., office space) allows me to focus on my work
There is plenty of natural light in my workplace
I can conveniently access nature in or close to my work environment (e.g., parks, nature preserves, etc)
My country's political and social climate provides a sense of safety and security
I'm regularly concerned about the negative consequences that the climate crisis will have on my life and the life of loved ones
I feel in control of my digital environment including notifications, social media, and other distractions
I know how to adequately manage my data and privacy online.

Make two questions that captures most of these elements in a simple way

---

> which of these? 
I am comfortable with my current income
I could lose several months of pay due to serious illness, and still have my economic security
In the event of a financial emergency, I have adequate savings
The economic situation of my country provides a helpful foundation for my personal financial security and stability

---

## 📝 Align Questions & Answers
**Date**: 2023-08-09 | **Source**: chatgpt

> we can also align with things we know, like a website should be a url and a founding date should be a date. these can help re-align our data. Let's take a multi-modal approach? Perhaps we can use some nltk to figure out if nationality is a noun and the nationality, etc. We map what we can and then fit the others between the gaps of the known things?

---

## 📝 Simpler Whisper Transcription.
**Date**: 2023-08-07 | **Source**: chatgpt

> I want to replace this more complex transcribe with a simpler one yet still return the segments with start, end, no speech prob, temperature, compression ratio and language, all the segment data.

---

## 📝 Fix Sun SVG Display
**Date**: 2023-08-04 | **Source**: chatgpt

> still getting these issues:
Element implicitly has an 'any' type because expression of type 'string' can't be used to index type '{ fajr: { backgroundColor: string; }; dawn: { backgroundColor: string; }; dhuhr: { backgroundColor: string; }; asr: { backgroundColor: string; }; maghrib: { backgroundColor: string; }; isha: { backgroundColor: string; }; lateNight: { ...; }; night: { ...; }; }'.
  No index signature with a parameter of type 'string' was found on type '{ fajr: { backgroundColor: string; }; dawn: { backgroundColor: string; }; dhuhr: { backgroundColor: string; }; asr: { backgroundColor: string; }; maghrib: { backgroundColor: string; }; isha: { backgroundColor: string; }; lateNight: { ...; }; night: { ...; }; }'.ts(7053)

---

> here's my styles.tsx;
import { StyleSheet } from 'react-native';

export const styles = StyleSheet.create({
  fajr: { backgroundColor: 'pink' },
  dawn: { backgroundColor: 'lightblue' },
  dhuhr: { backgroundColor: 'yellow' },
  asr: { backgroundColor: 'orange' },
  maghrib: { backgroundColor: 'purple' },
  isha: { backgroundColor: 'darkblue' },
  lateNight: { backgroundColor: 'black' },
  night: { backgroundColor: 'black' }
});

---

> sun position x and y is different:

  const textX = position.x.interpolate({
    inputRange: [0, radius * 2],
    outputRange: [0, radius * 2],
  });

  const textY = position.y.interpolate({
    inputRange: [0, radius * 2],
    outputRange: [0, radius * 2],
  });
  
  const getSunPosition = (radians) => {
    const x = radius - radius * Math.sin(radians);
    const y = radius - radius * Math.cos(radians);
    return { x, y };
  };

---

> connect this to the get sunposition funciton:

  const textX = position.x.interpolate({
    inputRange: [0, radius * 2],
    outputRange: [0, radius * 2],
  });

  const textY = position.y.interpolate({
    inputRange: [0, radius * 2],
    outputRange: [20, radius * 2 + 20], // Added an offset to move the text down
  });

---

> here's my styles.tsx:
import { StyleSheet } from 'react-native';

export const styles = StyleSheet.create({
  fajr: { backgroundColor: 'pink' },
  dawn: { backgroundColor: 'lightblue' },
  dhuhr: { backgroundColor: 'pink' },
  asr: { backgroundColor: 'orange' },
  maghrib: { backgroundColor: 'purple' },
  isha: { backgroundColor: 'darkblue' },
  lateNight: { backgroundColor: 'black' },
  night: { backgroundColor: 'black' }
});
rotation: {
  transform: [{ rotate: '-108deg' }]
}

---

> how do i add these styles? body.fajr {
    background: radial-gradient(circle at 50% 75%, lightpink, darkpink);
}

body.dawn {
    background: radial-gradient(circle at 50% 75%, lightrose, darkpink);
}

body.dhuhr {
    background: radial-gradient(circle at 50% 75%, lightyellow, lightrose);
}

body.asr {
    background: radial-gradient(circle at 50% 75%, yellow, lightyellow);
}

body.maghrib {
    background: radial-gradient(circle at 50% 75%, orange, yellow);
}

body.isha {
    background: radial-gradient(circle at 50% 75%, red, orange);
}

body.late-night {
    background: radial-gradient(circle at 50% 75%, midnightblue, red);
}

body.night {
    background: radial-gradient(circle at 50% 75%, midnightblue, black);
}

---

## 📝 Fixing App Prayer Times.
**Date**: 2023-08-03 | **Source**: chatgpt

> can you make this a tsx? // Utils.tsx

export const parseTime = (time) => {
    const [hours, minutes] = time.split(':');
    const date = new Date();
    date.setHours(parseInt(hours), parseInt(minutes), 0, 0);
    return date;
  };
  
  export const mapTimeToAngle = (time, times) => {
    const start = parseTime(times.Fajr);
    const end = parseTime(times.Isha);
    const current = parseTime(time);
    const angle = ((current - start) / (end - start) * (198 - (-18))) + (-18);
    return -angle;
  };


  export const mapTimeToRadians = (time: string, times: any) => {
    const angle = mapTimeToAngle(time, times);
    const scaledAngle = angle * (360 / 198);
    const radians = (scaledAngle - 90) * Math.PI / 180;
    return radians;
  };
  
  
  export const getCurrentTimeIn24HourFormat = () => {
    const currentTime = new Date();
    return currentTime.toTimeString().split(' ')[0];
  };

---

## 📝 D3.js Islamic Prayer Arcs
**Date**: 2023-07-28 | **Source**: chatgpt

> no i want it squished between those angles, canwe move the sun faster so a second moves faster, perhaps this much faster would make sense:  360/198

---

## 📝 Circle View: Muslim Prayer
**Date**: 2023-07-26 | **Source**: chatgpt

> 1 both and it's also currently broken
2 fine to move to other libraries

The arc creation component is broken so lets' fix that

function drawSunPath(times) {
    const segments = [
        { start: times.Fajr, end: times.Sunrise, color: 'pink' },
        { start: times.Sunrise, end: times.Dhuhr, color: 'lightblue' },
        { start: times.Dhuhr, end: times.Asr, color: 'yellow' },
        { start: times.Asr, end: times.Maghrib, color: 'orange' },
        { start: times.Maghrib, end: times.Isha, color: 'purple' },
        { start: times.Isha, end: times.Fajr_tomorrow, color: 'darkblue' },
    ];

    const line = d3.line().x(d => d.x).y(d => d.y);

    segments.forEach(segment => {
        const startAngle = mapTimeToAngle(segment.start, times);
        const endAngle = mapTimeToAngle(segment.end, times);
        const points = d3.range(startAngle, endAngle, 0.1).map(angle => {
            const radians = angle * Math.PI / 180;
            return { x: radius * Math.cos(radians), y: -radius * Math.sin(radians) };
        });
        svg.append('path').attr('d', line(points)).attr('stroke', segment.color).attr('stroke-width', 2).attr('fill', 'none');
    });

    const timePoints = ['Fajr', 'Sunrise', 'Dhuhr', 'Asr', 'Maghrib', 'Isha'];

    timePoints.forEach(time => {
        const angle = mapTimeToAngle(times[time], times);
        const radians = angle * Math.PI / 180;
        const x = radius * Math.cos(radians);
        const y = -radius * Math.sin(radians);
        const textAnchor = ["Asr", "Maghrib", "Isha"].includes(time) ? "start" : "end";
        const textX = ["Asr", "Maghrib", "Isha"].includes(time) ? x + 10 : x - 10;
        const textY = y < 0 ? y - 10 : y + 10;
        svg.append('text').attr('class', 'timeText').attr('x', textX).attr('y', textY).attr('text-anchor', textAnchor).text(time + ' ' + times[time]);
    });
}

---

> // Map a time to an angle
function mapTimeToAngle(time, times) {
    const start = parseTime(times.Fajr);
    const end = parseTime(addTime(times.Fajr, 24));
    const current = parseTime(time);
    const angle = (current - start) / (end - start) * 360;
    return angle;

} 

Should we fix the time/times name here it's confusing

---

## 📝 Update Lat Long.
**Date**: 2023-07-26 | **Source**: chatgpt

> it says "undefined" right by the sun for some reason. why isn't the circle centered? why isn't the sun higher in the sky it's almost asr now, Changing the sky color: We will create a gradient sky color based on the time of the day. We will make use of CSS linear gradients for the sky color.

Text color: We will update the color of the text based on the background color for better readability.

---

## 📝 Harvard vs PERMA
**Date**: 2023-07-25 | **Source**: chatgpt

> can you give it a best guess from what you know? perhaps social status using a standard from lower to upper class? education level from a standard list, I don't want specifics I want them all to be "standardized"

---

## 📝 Prayer Circle in Paris
**Date**: 2023-07-25 | **Source**: chatgpt

> fajir time shoul dbe just on the horizon just below the mid point horizon of the bigger circle with the line
You should also display current time

Draw a horizon line through the bigger circle with a thinline to indicate the horizon and move the red sun near the sunset area on the horizon line on the right because now it's near maghrib time

---

> nice horizon line and the sun is stuck in the upper left corner of the screen. right now it should be near the horizon line on the left. You can imagine the red ball moving on a larger invisible circle. Maybe best to make the larger circle the red sun ball moving on a light gray thin line so we can see where it moves center the larger thin gray one around the thin black one and move the sun along on the thin gray one. Don't forget the horizon line too

---

> I see the sun in the lower right hand side fo the "earth" and the background is blue when it should be more close to the white yellow of thuhur time. The text is randomly placed in the center, where would a ux professional put the text? Add some padding, make the text nice, modern font, nice light transparent background padding. And the simulate buttons do nothing now it seems, why are there three?

---

> why isn't the sun on the dotted line representing the sun's path? Also the sun is in the wrong spot still. At 11:55am it should be near the zenith between fajir and thuhur. Maybe something that can help us understand and debug is to make the dotted line thicker and to color each section according to it's time of day. For instance when the sun is at the zenith of the circle at thuhur time the dotted line segment should be yellow white, makes sense?

---

> ok, it's sort of working except the fajir is on the right hand side i want it all inverted 
function mapTimeToAngle(time, times) {
    const start = parseTime(times.Fajr);
    const end = parseTime(times.Isha);
    const current = parseTime(time);
    const angle = ((current - start) / (end - start) * (198 - (-18))) + (-18);
    return angle;
}
maybe here,

---

> i don't want that to be for the update, I want it to be on initialization picking your current ip based lat long

---

> this is what we had before that worked

        // Map a time to an angle
function mapTimeToAngle(time, times) {
    const start = parseTime(times.Fajr);
    const end = parseTime(times.Isha);
    const current = parseTime(time);
    const angle = ((current - start) / (end - start) * (198 - (-18))) + (-18);
    return angle;
}
        // Parse a time string into a Date object
        function parseTime(time) {
            const [hours, minutes] = time.split(':');
            const date = new Date();
            date.setHours(+hours);
            date.setMinutes(+minutes);
            return date;
        }

---

> i just see a left facing pacman. Also i want fajir to be at 8pm -18 degrees on the left and isha to be -18 on the right at 4pmish

---

## 📝 Activity Filters List
**Date**: 2023-07-24 | **Source**: chatgpt

> What are categories for activities that might be helpful for people to have as filters, including things like, duration of activity, number of people that can do it (alone, small groups, bigger groups), resource type, activity type (reading, filling a worksheet, what other types of things can be here?) etc, can you make me a list?

---

## 📝 Enhanced Assam Oud Experience
**Date**: 2023-07-17 | **Source**: chatgpt

> can you improve this message sent to someone who just bought our assam oud essential oil on our etsy apge? Bonjour Alberto!

Your order is flying out towards you - get your nose ready to enjoy a sensory trip with your new smell :)
If you'd like, you can sign up for our newsletter so we can let you know when we have coupons, new items and collaborations coming. You'll also get a 15% discount off your next order: http://bit.ly/NCSLetter 

Have a sweet day!
+NCS

---

> make this one nicer? Bonjour Daniel!

Your order is flying out towards you - get your nose ready to enjoy a sensory trip with your new smell :)
If you'd like, you can sign up for our newsletter so we can let you know when we have coupons, new items and collaborations coming. You'll also get a 15% discount off your next order: http://bit.ly/NCSLetter 

Have a sweet day!
+NCS

---

## 📝 Grant Overlap Identification
**Date**: 2023-07-15 | **Source**: chatgpt

> You are a professional grant writer helping us modify existing answers to questions in a table given a new grant opportunity. I will first give you the grant opportunity's question list and our question list and I want you to find the overlaps, ready?

---

## 📝 Kurdish Fellowship Proposal
**Date**: 2023-07-14 | **Source**: chatgpt

> More information: 
Regarding your question about who in the government should you send it to, you can send it to the Council of Ministers of the Kurdistan Regional Government. You can find their contact information on their website1.

As for who else might be interested in seeing this proposal, you can try reaching out to Kurdish Studies Research and Study Opportunities2 or Dr Veysi Dag3 who is currently researching the functions and politics of diverse Kurdish diaspora associations in European cities.

I hope this helps! Let me know if you have any other questions or if there’s anything else I can help you with.

---

## 📝 Scrape & Save Webpages
**Date**: 2023-07-14 | **Source**: chatgpt

> I have a folder with called docs with .md files with text in them, i want to combine all the text files into one file. there are subfolders, can you write a script to do that with python?

---

## 📝 Variable Speed Audio Enhancement
**Date**: 2023-07-13 | **Source**: chatgpt

> Great, let's make an early approach to make an audio book with variable speed from audio books on project guten berg. can you make a python script which takes in an audio book. identifies the right times to go faster and slower and to very smoothly ramp up and down between speed zones based on complexity. It should tag blocks of text by complexity and other elements it picks up from the text analysis. By doing concept analysis. Identifying complexity of concepts. and tagging each text block with meta data. Can you clarify the project and ask any questions you need to create a 1 page project description that i can send to a developer to help me share?

---

## 📝 Perfume Profiles & Notes.
**Date**: 2023-07-03 | **Source**: chatgpt

> Pull out the notes in this perfume and make a table to show a set of different types of perfume with a similar profile and the notes they need as a top/base/mid and be sure to include petrichor geosmine copper woody other types of essences:
Boisé 

Notes de tête :
Bergamote, Orange

Notes de coeur :
Huile d'amyris, Coriandre de Russie, Huile de bois d'agar

Notes de fond :
Bois de cèdre, Bois de santal, Huile de Patchouli, Accord de cuir, Musc

---

> Pull out the notes in this perfume and make a table to show a set of different types of perfume with a similar profile and the notes they need as a top/base/mid and be sure to include petrichor/ geosmine notes:
Boisé 

Notes de tête :
Bergamote, Orange

Notes de coeur :
Huile d'amyris, Coriandre de Russie, Huile de bois d'agar

Notes de fond :
Bois de cèdre, Bois de santal, Huile de Patchouli, Accord de cuir, Musc

---

## 📝 Swamp Cooler with New Materials
**Date**: 2023-06-24 | **Source**: chatgpt

> How can I take advantage of extreme hydrophobic coatings and vanta black while making a swamp cooler? How does an heat exchanger work? Peltiers? Ceramic evaporative cooling? 3D printed ceramic? I want a home ça that takes advantage of these new materials and techniques

---

## 📝 Developer Solution Concentration
**Date**: 2023-06-19 | **Source**: claude

> if i want a ratio of 1 to 14 developer yo watwr andbi want a rasult of 500ml of solutoon how kuch developer should i add to the water?

---

## 📝 New chat
**Date**: 2023-05-30 | **Source**: chatgpt

> ImportError: cannot import name 'Tokenizer' from 'tiktoken' (/Users/bilalghalib/mambaforge/envs/myenv/lib/python3.10/site-packages/tiktoken/__init__.py)
>>> 
KeyboardInterrupt
>>> exit()
(myenv) bilalghalib@macbook-pro streamChatPDF % pip install tiktoken
Requirement already satisfied: tiktoken in /Users/bilalghalib/mambaforge/envs/myenv/lib/python3.10/site-packages (0.4.0)
Requirement already satisfied: regex>=2022.1.18 in /Users/bilalghalib/mambaforge/envs/myenv/lib/python3.10/site-packages (from tiktoken) (2023.5.5)
Requirement already satisfied: requests>=2.26.0 in /Users/bilalghalib/mambaforge/envs/myenv/lib/python3.10/site-packages (from tiktoken) (2.31.0)
Requirement already satisfied: charset-normalizer<4,>=2 in /Users/bilalghalib/mambaforge/envs/myenv/lib/python3.10/site-packages (from requests>=2.26.0->tiktoken) (3.1.0)
Requirement already satisfied: idna<4,>=2.5 in /Users/bilalghalib/mambaforge/envs/myenv/lib/python3.10/site-packages (from requests>=2.26.0->tiktoken) (3.4)
Requirement already satisfied: urllib3<3,>=1.21.1 in /Users/bilalghalib/mambaforge/envs/myenv/lib/python3.10/site-packages (from requests>=2.26.0->tiktoken) (2.0.2)
Requirement already satisfied: certifi>=2017.4.17 in /Users/bilalghalib/mambaforge/envs/myenv/lib/python3.10/site-packages (from requests>=2.26.0->tiktoken) (2023.5.7)

---

> can you learn from this style so the conversation looks like a chat going vertically? 
import gradio as gr
import random
import time

def respond(message, chat_history):
    bot_message = random.choice(["How are you?", "I love you", "I'm very hungry"])
    chat_history.append((message, bot_message))
    time.sleep(1)
    return "", chat_history

iface = gr.Interface(
    fn=respond,
    inputs="textbox",
    outputs="text",
    description="conversation tool",
    layout='vertical'
)

iface.launch()

---

> no, it seems like it's installing them to different folders for differnt python versions I stillg et this error:  Using cached tiktoken-0.4.0-cp310-cp310-macosx_11_0_arm64.whl (761 kB)
Requirement already satisfied: regex>=2022.1.18 in /Users/bilalghalib/mambaforge/envs/myenv/lib/python3.10/site-packages (from tiktoken) (2023.5.5)
Requirement already satisfied: requests>=2.26.0 in /Users/bilalghalib/mambaforge/envs/myenv/lib/python3.10/site-packages (from tiktoken) (2.31.0)
Requirement already satisfied: charset-normalizer<4,>=2 in /Users/bilalghalib/mambaforge/envs/myenv/lib/python3.10/site-packages (from requests>=2.26.0->tiktoken) (3.1.0)
Requirement already satisfied: idna<4,>=2.5 in /Users/bilalghalib/mambaforge/envs/myenv/lib/python3.10/site-packages (from requests>=2.26.0->tiktoken) (3.4)
Requirement already satisfied: urllib3<3,>=1.21.1 in /Users/bilalghalib/mambaforge/envs/myenv/lib/python3.10/site-packages (from requests>=2.26.0->tiktoken) (2.0.2)
Requirement already satisfied: certifi>=2017.4.17 in /Users/bilalghalib/mambaforge/envs/myenv/lib/python3.10/site-packages (from requests>=2.26.0->tiktoken) (2023.5.7)
Installing collected packages: tiktoken
Successfully installed tiktoken-0.4.0
(myenv) bilalghalib@macbook-pro streamChatPDF % python -V             
Python 3.10.11
(myenv) bilalghalib@macbook-pro streamChatPDF % which python
/Users/bilalghalib/mambaforge/envs/myenv/bin/python

You see when I install it immediately after uninstalling it says that "Requirement already satisfied" how can I install it for this python 3.10.11 in mambaforge/envs/myenv...

---

## 📝 New chat
**Date**: 2023-05-26 | **Source**: chatgpt

> Issue ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.
web3 5.31.4 requires protobuf==3.19.5, but you have protobuf 3.20.3 which is incompatible.
web3 5.31.4 requires websockets<10,>=9.1, but you have websockets 11.0.3 which is incompatible.

---

## 📝 Resolving Python Package Conflicts
**Date**: 2023-05-26 | **Source**: chatgpt

> error: ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.
web3 5.31.4 requires protobuf==3.19.5, but you have protobuf 3.20.3 which is incompatible.
web3 5.31.4 requires websockets<10,>=9.1, but you have websockets 11.0.3 which is incompatible.

---

> Successfully uninstalled protobuf-3.20.3
ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.
tensorboard 2.13.0 requires protobuf>=3.19.6, but you have protobuf 3.19.5 which is incompatible.
tensorflow-hub 0.13.0 requires protobuf>=3.19.6, but you have protobuf 3.19.5 which is incompatible.
tensorflow-macos 2.13.0rc0 requires protobuf!=4.21.0,!=4.21.1,!=4.21.2,!=4.21.3,!=4.21.4,!=4.21.5,<5.0.0dev,>=3.20.3, but you have protobuf 3.19.5 which is incompatible.

---

## 📝 Potting Mix Project Overview
**Date**: 2023-05-25 | **Source**: chatgpt

> summarize this in English: مشكلة النفايات التي بلغت ذروتها في لبنان في الاونة الاخيرة في اظل الوضع الاقتصادي والتفلت الامني وعدم اهتمام الدولة بالمتابعة او بحل هذه المشكلة ، وانا كبيولوجية اعلم مدى تاثير النفايات والتلوث على المناخ وعلى الحياة في البر والبخر قررت القيام بهذه المبادة والتاثيؤ قدر الامكان ، لا احد.سينقذنا من الغرق في النفايات ان لم ننقذ انفسنا

---

> summarize in English تعاني المنطقة من الافتقار للانتاج الزراعي والمحاصيل الزراعية بسبب طبيعة البلاد الجبلية وعدم توفر المياه باغلب المناطق ومشروعي عم يحل مشكلة كبيرة بالمنطقة وهي افتقار للمنتج الصحي منتجي عم يكون محلي الصنع عم يكون إنتاجنا محلي واكتفاءنا ذاتي منتج صحي مشبع بالفيتامينات والبروتينات والمعادن النافعة خالي من الهرمونات والمواد الكيميائية منتج صحي نظيف

---

> summarize in English تعاني المنطقة من الافتقار للانتاج الزراعي والمحاصيل الزراعية بسبب طبيعة البلاد الجبلية وعدم توفر المياه باغلب المناطق ومشروعي عم يحل مشكلة كبيرة بالمنطقة وهي افتقار للمنتج الصحي منتجي عم يكون محلي الصنع عم يكون إنتاجنا محلي واكتفاءنا ذاتي منتج صحي مشبع بالفيتامينات والبروتينات والمعادن النافعة خالي من الهرمونات والمواد الكيميائية منتج صحي نظيف

---

> summarize in English: تربية الدواجن بالأعشاب والطب البديل
تتلخص فكرة المشروع في تربية الدواجن اللاحمة علي الأعشاب الطبيعية من خلال إضافتها  الي الأعلاف المقدمة للدواجن  دون اللجوء لأي حقن كيماوية الذي توثر علي صحة المستهلكين بالعديد من الأمراض القلبية وأمراض الكلي والكبد  وهذه الأعشاب لها أهمية كبيرة للدواجن منها ترفع المناعة وتزود البكتيريا النافعة وتطهر الأمعاء وتعزز عملية الهضم وتعالج الكوكسيديا وبعض الأعشاب تحتوي علي البوتاسيوم والفسفور وفاتحة للشهية والعديد من الفوائد التي لا حصر لها وأهم ما سيميز هذه الدواجن هو فرق المذاق حيث أنني سأقدم منتجات صحية وصديقة للأسرة وللبيئة ويعتمد مشروعي علي مبدأ الوقاية خير من العلاج فهذه الأعشاب تعطي للدواجن لإكسابهم مناعة جيدة لمقاومة الأمراض مما يجعلني غير محتاجة لأي ادوية كيماوية او بيولوجية

---

> summarize in English: منطقة عرسال اللبنانية التي تضم أكبر عدد من النازحين بنسبة 70الف ويبلغ عدد سكانها الأصل 45 الف حيث يصبح العدد الكلي 115 الف حسب إحصائيات بلدية عرسال بعد جائحة كورونا والحجر الصحي وفرض وزير التعليم قرار بتسكير المدارس ونقل التعليم عبر الانترنت من هنا ظهر ضعف المهارات والخبرة التقنية لدى الطلاب والأهلي مما أدى الى تسريب الطلاب في تلك الفترة وذلك أدى إلى وجود طلاب من جميع المراحل لا يملكون خبرات ومهارات في التقنيات وأيضا عدم القدرة على اكتساب مهارات مهنية وتعليمية كما قالت أحدى شهود العيان (ن.م) خلال دراستنا للخريطة المجتمعية بعد ما صار التعليم عبر الانترنت واجهة كتير صعوبة بتعليم أطفالي وهل شي خلاني وقف تدريسهم عبر الإنترنت ليرجعو يفتحو المدارس وكان من أكبر سلبيات جائحة كورونا تفشي الفقر و تدهور الوضع الاقتصادي لعدم قدرة الأشخاص المعيلة على ممارسة أعمالهم

---

> translate: اولويتنا ادخال تدريبات الفنون جديدة الى المنطقة (مسرح وموسيقا) نطمح لتدريب فريق مسرحي واخر موسيقي وانشاء عروض تسلط الضوء على مشكلات مجتمع  وايضا تدريباتنا التى تضم تدريبات كمبيوتر وتصوير ومونتاج وزيادة خبرة الشباب والشابات في المنطقة وتوفير الوقت والجهد بسبب صعوبة الحصول على هذه التدريبات ضمن عرسال  وايضا مهتمين بجانب التوعوية ويضم نشاطات اطفال ترفيهية وتعليمية وجلسات توعية حول الجندر والادوار الجندرية والعنف القائم 
 على النوع الاجتماعي

---

## 📝 Employment Verification Letter Revision
**Date**: 2023-05-23 | **Source**: chatgpt

> Can you fix this template? 
To whom it may concern,

We certify that Mr. Ghalib Bilal is employed by the company <Company name>, registered in <City> under the number <SIRET of the company>, domiciled at <Address of the head office>, as <Title of the workstation> on a permanent contract since <Date of hiring>.

He receives a gross annual salary of <Amount> euros and works a weekly schedule of <Number of hours> hours.


Mr. Ghalib Bilal is not currently in a period of notice, dismissal or resignation or in the process of being transferred.

We ask you to believe, Madam, Sir, in the expression of our distinguished greetings.

Done at <City>, on May 23rd 2023.

Made to serve and assert what is right

<Name and first name>
<Function>
<Signature + company stamp>

---

## 📝 Eventlet Server Error Fix
**Date**: 2023-05-23 | **Source**: chatgpt

> I don't want to do that, I want to send the stream as it comes in real time so it streams one word at a time on the other side

---

> how can I test that this is happening?

    eventSource.onmessage = (event) => {
      console.log('Received message:', event.data);

      const botMessage = {
        role: 'DataBot',
        content: event.data,
      };

      setMessages((messages) => [...messages, botMessage]);
    };
It seems like this console.log never triggers. although the curl seemed to work at that endpoint, weird right?

---

> and this error in the console: < (err) => {
  console.error('Error:', err);
}
[Error] Error: – Event {isTrusted: true, type: "error", target: EventSource, …}

Event {isTrusted: true, type: "error", target: EventSource, currentTarget: EventSource, eventPhase: 2, …}Event
	(anonymous function) (client.js:2:918)
	(anonymous function) (next-dev.js:27)
	Console Evaluation (Console Evaluation 1:14)

---

## 📝 Project Over Budget Discussion
**Date**: 2023-05-22 | **Source**: chatgpt

> help me say this in a professional business manner: I wound up talking to Agha about where the issue arose and it seemed it was clear to him where he misunderstood the assignment. We didn’t talk about the budget and right now we are already over budget for building the wrong thing and  I’m not willing to pay to do the initial task from scratch. Let me know what makes sense as this project is already over the cost I allocated for it.

---

## 📝 Chat App Development Plan
**Date**: 2023-05-21 | **Source**: chatgpt

> where does this info go? import os

it's in the current config.py 

from dotenv import load_dotenv
from flask import Flask
from celery import Celery

load_dotenv()

app = Flask(__name__)

app.config['CELERY_BROKER_URL'] = os.getenv('CELERY_BROKER_URL')
app.config['CELERY_RESULT_BACKEND'] = os.getenv('CELERY_RESULT_BACKEND')

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

---

> issue now: Traceback (most recent call last):
  File "/Users/bilalghalib/Projects/scripts/chatOnTask/chat-with-data/app.py", line 8, in <module>
    serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])
  File "/Users/bilalghalib/mambaforge/lib/python3.10/site-packages/itsdangerous/serializer.py", line 104, in __init__
    self.secret_keys: _t.List[bytes] = _make_keys_list(secret_key)
  File "/Users/bilalghalib/mambaforge/lib/python3.10/site-packages/itsdangerous/signer.py", line 64, in _make_keys_list
    return [want_bytes(s) for s in secret_key]
TypeError: 'NoneType' object is not iterable

---

> still getting errors
t iterable
(base) bilalghalib@MacBook-Pro chat-with-data % python app.py
Traceback (most recent call last):
  File "/Users/bilalghalib/Projects/scripts/chatOnTask/chat-with-data/app.py", line 10, in <module>
    app = Flask(__name__)
NameError: name 'Flask' is not defined
(base) bilalghalib@MacBook-Pro chat-with-data %

---

> server is here:
const express = require('express');
const axios = require('axios');
const app = express();
const port = 3000;

app.use(express.json()); // for parsing application/json

app.get('/stream_chat', (req, res) => {
    axios.post('http://127.0.0.1:5011/stream_chat', { messages: [{ role: 'user', content: 'Hello, world!' }] }, { responseType: 'stream' })
        .then(response => {
            response.data.pipe(res);
        })
        .catch(error => {
            console.error(error);
        });
});

app.post('/stream_chat', (req, res) => {
    const messages = req.body.messages;
    axios.post('http://127.0.0.1:5011/stream_chat', { messages })
        .then(response => {
            res.json(response.data);
        })
        .catch(error => {
            console.error(error);
        });
});

app.listen(port, () => {
    console.log(`Node.js server listening at http://127.0.0.1:${port}`);
});
Running well:
(base) bilalghalib@MacBook-Pro client % node server.js
Node.js server listening at http://127.0.0.1:3000

---

> this is our current server:
const express = require('express');
const cors = require('cors');
const app = express();

app.use(cors());  // This will enable CORS for all routes

const port = 3000;

app.use(express.json()); // for parsing application/json

app.get('/stream_chat', (req, res) => {
    axios.post('http://127.0.0.1:5011/stream_chat', { messages: [{ role: 'user', content: 'Hello, world!' }] }, { responseType: 'stream' })
        .then(response => {
            response.data.pipe(res);
        })
        .catch(error => {
            console.error(error);
        });
});

app.post('/stream_chat', (req, res) => {
    const messages = req.body.messages;
    axios.post('http://127.0.0.1:5011/stream_chat', { messages })
        .then(response => {
            res.json(response.data);
        })
        .catch(error => {
            console.error(error);
        });
});

app.listen(port, () => {
    console.log(`Node.js server listening at http://127.0.0.1:${port}`);
});
can you update it with socket io stuff and tell me what to install with pip?

---

> it's giving me one word at a time followed by a carriage return, I want it to stream as a single string

---

> so now the history and conversation is saved and displayed well, except I want the string to stream all into one string like before before getting saved as an entire response into the message history. 
you see it looks like this now:
User: yeah? what's good tell me a joke

DataBot: Why

DataBot: don

DataBot: 't

DataBot: scientists

DataBot: trust

DataBot: atoms

DataBot: ?

DataBot: Because
which is wrong

---

> it's doing this in the chat. I want it to present the text one at a time and then store the variable in the message array at the end. now I see every step:
Stream Chat
User: hi dear

DataBot: Hello

DataBot: Hello!

DataBot: Hello! How

DataBot: Hello! How can

DataBot: Hello! How can I

DataBot: Hello! How can I assist

DataBot: Hello! How can I assist you

DataBot: Hello! How can I assist you today

DataBot: Hello! How can I assist you today?

---

## 📝 Refactoring Chrome Plugin Code
**Date**: 2023-05-20 | **Source**: chatgpt

> can you create a 
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.message === "getConversationHistory") {
        chrome.runtime.sendMessage({ message: "updateConversationHistory", conversationHistory });
    } called 
logToServiceWorkerConsole
That accèpts 
        chrome.runtime.sendMessage({ message: "logToServiceWorkerConsole", data: conversationHistory });

and prints it to the service worker log?

---

> does this mean that I need to have "conversation history" be in single quotes here:

            chrome.storage.local.set({conversationHistory: message.conversationHistory}, function() {
                chrome.runtime.sendMessage({ message: "logToServiceWorkerConsole", data: "Popup.js Saved conversation history in local storage" });
                displayConversationHistory();
            });

---

## 📝 "Disabling User Input Temporarily"
**Date**: 2023-05-20 | **Source**: chatgpt

> I want the gather tasks to start from popup.js not serviceworker - it should start when someone clicks the startPrioritizationButton button

---

> how do I run the displayconversationhistory functinoonly after the first one is done as it's async:

        else if (message.message === "tasksGathered") {
              console.log("Tasks received from foreground script:", message.tasks);
              // Send the tasks to the service worker
              chrome.runtime.sendMessage({ message: "tasksGatheredService", tasks: message.tasks });
              displayConversationHistory();
            }

---

## 📝 "Updating Agent Relevancy Score"
**Date**: 2023-05-20 | **Source**: chatgpt

> I want it to calculate the relevancy score as soon as the agents are created on instantiation of the agent.

---

## 📝 Code Error Fixing; Improving Agent Initialization
**Date**: 2023-05-20 | **Source**: claude

> do I need to add it to init?

class Agent:

def **init**(self, parliament, agent\_name, speaking\_pressure\_increment, initial\_context, agent\_type, agent\_instance, websocket=None):

self.speaking\_pressure\_increment = speaking\_pressure\_increment

self.name = agent\_name

self.context = initial\_context

self.initial\_context = initial\_context

self.agent\_type = agent\_type

self.agent\_instance = agent\_instance

self.websocket = websocket

self.parliament = parliament

self.relevancy\_score = None

def set\_typing\_status(self, status: bool):

self.is\_typing = status

---

> does it also need to go into the def **init**(self, parliament, agent\_name, speaking\_pressure\_increment, initial\_context, agent\_type, agent\_instance, websocket=None): line

So something like

def **init**(self, parliament, agent\_name, speaking\_pressure\_increment, initial\_context, agent\_type, agent\_instance, is\_typing,

websocket=None):

---

> we already have a list of agents, why not get the string from inside the agent class inside the list?

class Parliament:

def **init**(self, name: str): # Added name argument

self.name = name # Added this line to store the name

self.agents: List\[Agent\] = \[\]

Agent class:

class Agent:

def **init**(self, parliament, agent\_name, speaking\_pressure\_increment, initial\_context, agent\_type, agent\_instance, is\_typing, websocket=None):

self.speaking\_pressure\_increment = speaking\_pressure\_increment

self.name = agent\_name

self.context = initial\_context

self.initial\_context = initial\_context

self.agent\_type = agent\_type

self.agent\_instance = agent\_instance

self.websocket = websocket

self.parliament = parliament

self.relevancy\_score = None

self.is\_typing = is\_typing

Couldn't we do something like:

def identify\_and\_tag\_mentioned\_agents(self, message):

mentioned\_agents = \[\]

for agent in self.agents:

if '@'+agent.name in message: <

\- (like this?)

mentioned\_agents.append(agent\_name)

self.agents\[agent\_name\].speaking\_pressure = SPEAKING\_PRESSURE\_LIMIT

self.agents\[agent\_name\].tagged = True

return mentioned\_agents

---

## 📝 "Service Worker Code Fixes"
**Date**: 2023-05-19 | **Source**: chatgpt

> when does the // sendRequestToServer function
sendRequestToServer(message.userMessage).then(data => {
    console.log(data);
    chrome.runtime.sendMessage({ message: "updateConversationHistory", conversationHistory });
});
Get called in the service worker.js 
It should only get called when we get an assistant message back from the server
Basically from here:
        conversationHistory.push({ "role": "assistant", "content": result_1.data.choices[0].message.content });

---

> I want it in the conversation history. I just don't want it displayed. It's sort of a secret priming message for the agent the user shouldn't see

---

## 📝 API Call and GPT-3 Chat Completion Code
**Date**: 2023-05-19 | **Source**: claude

> NameError
=========

NameError: name 'json' is not defined

Traceback _(most recent call last)_
-----------------------------------

*   File "/usr/local/lib/python3.8/site-packages/flask/app.py", line _2213_, in `__call__`
    
        return self.wsgi_app(environ, start_response)
    
*   File "/usr/local/lib/python3.8/site-packages/flask/app.py", line _2193_, in `wsgi_app`
    
        response = self.handle_exception(e)
    
*   File "/usr/local/lib/python3.8/site-packages/flask/app.py", line _2190_, in `wsgi_app`
    
        response = self.full_dispatch_request()
    
*   File "/usr/local/lib/python3.8/site-packages/flask/app.py", line _1486_, in `full_dispatch_request`
    
        rv = self.handle_user_exception(e)
    
*   File "/usr/local/lib/python3.8/site-packages/flask/app.py", line _1484_, in `full_dispatch_request`
    
        rv = self.dispatch_request()
    
*   File "/usr/local/lib/python3.8/site-packages/flask/app.py", line _1469_, in `dispatch_request`
    
        return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)
    
*   File "/usr/local/lib/python3.8/site-packages/flask\_cors/decorator.py", line _128_, in `wrapped_function`
    
        resp = make_response(f(*args, **kwargs))
    
*   File "/app/app.py", line _91_, in `result`
    
        response = generate_text.AsyncResult(task_id).get()

---

> AttributeError
==============

AttributeError: text

Traceback _(most recent call last)_
-----------------------------------

*   File "/usr/local/lib/python3.8/site-packages/flask/app.py", line _2213_, in `__call__`
    
        return self.wsgi_app(environ, start_response)
    
*   File "/usr/local/lib/python3.8/site-packages/flask/app.py", line _2193_, in `wsgi_app`
    
        response = self.handle_exception(e)
    
*   File "/usr/local/lib/python3.8/site-packages/flask/app.py", line _2190_, in `wsgi_app`
    
        response = self.full_dispatch_request()
    
*   File "/usr/local/lib/python3.8/site-packages/flask/app.py", line _1486_, in `full_dispatch_request`
    
        rv = self.handle_user_exception(e)
    
*   File "/usr/local/lib/python3.8/site-packages/flask/app.py", line _1484_, in `full_dispatch_request`
    
        rv = self.dispatch_request()
    
*   File "/usr/local/lib/python3.8/site-packages/flask/app.py", line _1469_, in `dispatch_request`
    
        return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)
    
*   File "/usr/local/lib/python3.8/site-packages/flask\_cors/decorator.py", line _128_, in `wrapped_function`
    
        resp = make_response(f(*args, **kwargs))
    
*   File "/app/app.py", line _92_, in `result`
    
        response = generate_text.AsyncResult(task_id).get()

---

## 📝 Fixing Code Errors; Improving Task Organization
**Date**: 2023-05-18 | **Source**: claude

> service-worker.js:1 Uncaught (in promise) Error: Could not establish connection. Receiving end does not exist.

Popup.js

function initializePopupScript() {

const button = document.getElementById("getTasksButton");

button.addEventListener("click", function() {

chrome.runtime.sendMessage({message: "goServiceWorker"});

});

}

document.addEventListener("DOMContentLoaded", initializePopupScript);

Serviceworker.js

// This is the service worker script, which executes in its own context

// when the extension is installed or refreshed (or when you access its console).

// It would correspond to the background script in chrome extensions v2.

console.log("This prints to the console of the service worker (background script)")

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {

if (message.message === "goServiceWorker") {

// Find the active tab

chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {

// If no tabs match the query

if (!tabs.length) {

console.log("No active tabs found.");

return;

}

const tab = tabs\[0\];

// If the tab hasn't finished loading

if (tab.status !== "complete") {

console.log("Active tab has not finished loading.");

return;

}

// Send message to the active tab's content script

console.log("We in service.");

chrome.tabs.sendMessage(tab.id, {message: "goForeground"});

});

}

});

// Importing and using functionality from external files is also possible.

importScripts('service-worker-utils.js')

// If you want to import a file that is deeper in the file hierarchy of your

// extension, simply do `importScripts('path/to/file.js')`.

// The path should be relative to the file `manifest.json`.

Foreground.js

console.log("This prints to the console (foreground script)")

chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {

if (request.message === "goForeground") {

console.log("We in foreground and button was clicked!");

}

});

---

## 📝 Songs of Strength
**Date**: 2023-05-15 | **Source**: claude

> Keep going! This one is an

excellent example:

1.  2008 | Man on Wire | Biography/Documentary | **Man on Wire on Tubi** | Tightrope walker Philippe Petit fulfills a dream, showing creativity, passion, leadership. | Creativity, Zest, Leadership 2008 | Man on Wire | Biography/Documentary | **Man on Wire on Tubi** | Tightrope walker Philippe Petit fulfills a dream, showing creativity, passion, leadership. | Creativity, Zest, Leadership

---

## 📝 Calculating Relevancy in a Single Loop
**Date**: 2023-05-13 | **Source**: claude

> can you give me the whole async def get\_agents\_info(self) -> List\[dict\]:?

Here's what I got so far:

async def get\_agents\_info(self) -> List\[dict\]:

agents\_info = \[\]

for agent\_name, agent in self.agents.items():

agents\_info.append({

"name": agent\_name,

"speaking\_pressure": agent.speaking\_pressure,

"speaking\_pressure\_increment": agent.speaking\_pressure\_increment,

"context": agent.context,

"agent\_type": agent.agent\_type,

"relevancy\_score": agent.relevancy\_score # Return the actual score here

})

return agents\_info

---

## 📝 GPT3 Relevancy Calculation
**Date**: 2023-05-12 | **Source**: chatgpt

> also that doesn't seem good, I want the message to davinci to be something like: "Given this agents initial context {initial context}, and the last 2000 tokens of the chat (limit the number of tokens we send to something davinci can handle) - how relevant do you think they are to the current conversation from 0 to 100. For instance if the current conversation is talking about feelings and the agent is the persona of a psychologist they will have a very high relevancy.

---

> can you modify this function to add agents as a dictionary object:
    def add_agent(self, agent: Agent):
        self.agents[agent.name] = agent
        self.typing_status[agent.name] = False  # Initialize typing status when adding an agent
        asyncio.create_task(agent.increment_pressure())

---

## 📝 Chat Protocol Improvements
**Date**: 2023-05-12 | **Source**: claude

> I want the opposite, I want it to put the cursor in the text box when I first load and each time the user clicks reply

---

## 📝 Relevancy-based Agent Response Selection
**Date**: 2023-05-12 | **Source**: claude

> Can you help me update this function:

function handleReceiveMessage(event) {

const data = JSON.parse(event.data);

const { action, message, sender, updated\_agents, queue } = data;

if (action === "receive\_message") {

console.log("data received")

console.log(data)

setMessages((prevMessages) => \[

...prevMessages.filter((message) => message.sender !== parliament.username || message.text !== "typing..."),

{ sender, text: message },

\]);

} else if (action === "typing" && sender !== parliament.username) {

setMessages((prevMessages) => \[

...prevMessages.filter((message) => message.sender !== sender || message.text !== "typing..."),

{ sender, text: "typing..." },

\]);

} else if (action === "update\_queue") {

setSpeakingQueue(queue);

}

if (updated\_agents) {

setAgents(updated\_agents);

}

}

with the handelrecievemessage you sent me?

function handleReceiveMessage(event) { ... if (action === "update\_agents") { setAgents(updated\_agents); // Update agent info state } }

?

---

## 📝 Agent Speaking Logic Update
**Date**: 2023-05-11 | **Source**: chatgpt

> I want the chat.js to send a "stopped typing" when it triggers its two seconds and for that to be the message sent to parliament from server.py

---

> WebSocket server is running on ws://localhost:8080
Queue updated: <parliament.SpeakingQueue object at 0x107129660>
Queue updated: <parliament.SpeakingQueue object at 0x107129660>
Queue updated: <parliament.SpeakingQueue object at 0x107129660>
Task exception was never retrieved
future: <Task finished name='Task-19' coro=<Parliament.broadcast_message() done, defined at /Users/bilalghalib/Projects/scripts/Parliment/parliament-chat-nextjs/pages/parliament_backend/parliament.py:207> exception=AttributeError("'SpeakingQueue' object has no attribute 'append'")>
Traceback (most recent call last):
  File "/Users/bilalghalib/Projects/scripts/Parliment/parliament-chat-nextjs/pages/parliament_backend/parliament.py", line 211, in broadcast_message
    self.update_speaking_queue()
  File "/Users/bilalghalib/Projects/scripts/Parliment/parliament-chat-nextjs/pages/parliament_backend/parliament.py", line 324, in update_speaking_queue
    self.speaking_queue.append(most_relevant_agent.name)
AttributeError: 'SpeakingQueue' object has no attribute 'append'

---

> Queue updated: <parliament.SpeakingQueue object at 0x1047cd870>
Queue updated: <parliament.SpeakingQueue object at 0x1047cd870>
Queue updated: <parliament.SpeakingQueue object at 0x1047cd870>
Task exception was never retrieved
future: <Task finished name='Task-22' coro=<Parliament.broadcast_message() done, defined at /Users/bilalghalib/Projects/scripts/Parliment/parliament-chat-nextjs/pages/parliament_backend/parliament.py:210> exception=AttributeError("'SpeakingQueue' object has no attribute 'pop'")>
Traceback (most recent call last):
  File "/Users/bilalghalib/Projects/scripts/Parliment/parliament-chat-nextjs/pages/parliament_backend/parliament.py", line 214, in broadcast_message
    self.update_speaking_queue()
  File "/Users/bilalghalib/Projects/scripts/Parliment/parliament-chat-nextjs/pages/parliament_backend/parliament.py", line 332, in update_speaking_queue
    self.trigger_next_speaker()
  File "/Users/bilalghalib/Projects/scripts/Parliment/parliament-chat-nextjs/pages/parliament_backend/parliament.py", line 320, in trigger_next_speaker
    next_speaker = self.get_agent(self.speaking_queue.pop(0))  # Remove the agent from the queue
AttributeError: 'SpeakingQueue' object has no attribute 'pop'

---

> future: <Task finished name='Task-22' coro=<Parliament.broadcast_message() done, defined at /Users/bilalghalib/Projects/scripts/Parliment/parliament-chat-nextjs/pages/parliament_backend/parliament.py:216> exception=TypeError('SpeakingQueue.pop() takes 1 positional argument but 2 were given')>
Traceback (most recent call last):
  File "/Users/bilalghalib/Projects/scripts/Parliment/parliament-chat-nextjs/pages/parliament_backend/parliament.py", line 220, in broadcast_message
    self.update_speaking_queue()
  File "/Users/bilalghalib/Projects/scripts/Parliment/parliament-chat-nextjs/pages/parliament_backend/parliament.py", line 338, in update_speaking_queue
    self.trigger_next_speaker()
  File "/Users/bilalghalib/Projects/scripts/Parliment/parliament-chat-nextjs/pages/parliament_backend/parliament.py", line 326, in trigger_next_speaker
    next_speaker = self.get_agent(self.speaking_queue.pop(0))  # Remove the agent from the queue
TypeError: SpeakingQueue.pop() takes 1 positional argument but 2 were given

---

## 📝 Align Chat Message Styles
**Date**: 2023-05-11 | **Source**: chatgpt

> <Mention
                trigger="@"
                data={agentNames}
                displayTransform={(id, display) => `@${display}`}
                style={{...defaultMentionStyle, color: 'black'}} // styles for the mentions
              />
            </MentionsInput> 
does this use color black of defaultmentionstyle?

---

## 📝 New chat
**Date**: 2023-05-11 | **Source**: chatgpt

> add what will take care of this issue:
he error message indicates that the Parliament object does not have an attribute called current_speaker. It seems that current_speaker is being used in the decide_next_speaker method without being defined anywhere. You may want to define current_speaker as an attribute of the Parliament object and initialize it appropriately.

---

> it seems like that's how its set up know:

            for agent_data in agents_data:
                agent_name = agent_data.get("name")
                speaking_pressure_increment = int(agent_data.get("speaking_pressure_increment"))
                other_agents = ", ".join([agent['name'] for agent in agents_data if agent['name'] != agent_name])
                context = (
                    f"Hello assistant, your name is: {agent_data.get('name')} and your context is "
                    f"{agent_data.get('context')}. Your job is to help {username} by discussing {topic} "
                    f"alongside your fellow agents in a parliament, which is a sort "
                    f"of town hall or large meeting, called {parliament.name}. The other agents discussing "
                    f"with you are {other_agents}. Give your best effort to help {username} by participating "
                    f"in a discussion with them and the other agents. Your talkativity is "
                    f"{agent_data.get('speaking_pressure_increment')} out of 100"
                )
                print ("context for agent")
                print (context)
                agent_type = agent_data.get("type")
                parliament.add_agent(agent_type, agent_name, speaking_pressure_increment, context, websocket)
            asyncio.create_task(parliament.agents_introduction())

---

> Task exception was never retrieved
future: <Task finished name='Task-13' coro=<Parliament.broadcast_message() done, defined at /Users/bilalghalib/Projects/scripts/Parliment/parliament-chat-nextjs/pages/parliament_backend/parliament.py:177> exception=NameError("name 'random' is not defined")>
Traceback (most recent call last):
  File "/Users/bilalghalib/Projects/scripts/Parliment/parliament-chat-nextjs/pages/parliament_backend/parliament.py", line 192, in broadcast_message
    self.speaking_queue = sorted(self.agents.keys(), key=lambda x: self.agents[x].calculate_relevancy(self.chat_history), reverse=True)
  File "/Users/bilalghalib/Projects/scripts/Parliment/parliament-chat-nextjs/pages/parliament_backend/parliament.py", line 192, in <lambda>
    self.speaking_queue = sorted(self.agents.keys(), key=lambda x: self.agents[x].calculate_relevancy(self.chat_history), reverse=True)
  File "/Users/bilalghalib/Projects/scripts/Parliment/parliament-chat-nextjs/pages/parliament_backend/parliament.py", line 111, in calculate_relevancy
    return random.randint(0, 100)
NameError: name 'random' is not defined

---

## 📝 Queue Update and Tagging
**Date**: 2023-05-11 | **Source**: chatgpt

> get this error: ^CTraceback (most recent call last):
  File "/Users/bilalghalib/Projects/scripts/Parliment/parliament-chat-nextjs/pages/parliament_backend/server.py", line 132, in <module>
    server.run()
  File "/Users/bilalghalib/Projects/scripts/Parliment/parliament-chat-nextjs/pages/parliament_backend/server.py", line 127, in run
    asyncio.get_event_loop().run_forever()
  File "/Users/bilalghalib/mambaforge/lib/python3.10/asyncio/base_events.py", line 603, in run_forever
    self._run_once()
  File "/Users/bilalghalib/mambaforge/lib/python3.10/asyncio/base_events.py", line 1871, in _run_once
    event_list = self._selector.select(timeout)
  File "/Users/bilalghalib/mambaforge/lib/python3.10/selectors.py", line 562, in select
    kev_list = self._selector.control(None, max_ev, timeout)
KeyboardInterrupt

---

## 📝 React Code Refactoring
**Date**: 2023-05-11 | **Source**: chatgpt

> got this error: <div><div style="position: relative; box-sizing: border-box; width: 100%; color: transparent; overflow: hidden; white-space: pre-wrap; overflow-wrap: break-word; border: 1px solid transparent; text-align: start;"><span style="visibility: hidden;">@</span> </div><textarea placeholder="Type your message..." style="display: block; width: 100%; position: absolute; margin: 0px; top: 0px; left: 0px; box-sizing: border-box; background-color: transparent; font-family: inherit; font-size: inherit; letter-spacing: inherit; height: 100%; bottom: 0px; overflow: hidden; resize: none;">@</textarea></div>

---

## 📝 Lettre de motivation locative
**Date**: 2023-05-10 | **Source**: chatgpt

> Can you write a letter of motivation to convince a landlord that we are great guests. We are a couple expecting our first baby. We're both professionals holding long term jobs at the same company for many years, we don't drink or smoke and don't like loud music. We are kind and like to cook and are excited to live together in lille near a park that will be nice for our baby. Write it in a way that would motivate the realtor and the landlord, what might they like to hear. keep it to half a page and can you do it in French in the style of a young professional

---

## 📝 Motivational Rental Application Letter
**Date**: 2023-05-10 | **Source**: chatgpt

> Can you write a letter of motivation to convince a landlord that we are great guests. We are a couple expecting our first baby. We're both professionals holding long term jobs at the same company for many years, we don't drink or smoke and don't like loud music. We are kind and like to cook and are excited to live together in lille near a park that will be nice for our baby. Write it in a way that would motivate the realtor and the landlord, what might they like to hear. keep it to half a page

---

## 📝 New chat
**Date**: 2023-05-10 | **Source**: chatgpt

> it says [Log] WebSocket connection opened in _app.js
and then in index.js it logs that we are "in use effect" and the web socket yet it doesn't log
"web socket connection opened in index.js"
why?
[Log] in use effect

[Log] WebSocket {listeners: Object, url: "ws://localhost:8080/", readyState: 1, bufferedAmount: 0, onopen: function, …}

---

> why is app.js closing the socket after testing to see if it's open?
import 'bootstrap/dist/css/bootstrap.min.css';
import '../styles/globals.css';
import { useState, useEffect } from 'react';
import Home from './index';

function MyApp({ Component, pageProps }) {
  const [websocket, setWebsocket] = useState(null);

  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8080');

    ws.onopen = () => {
      console.log("WebSocket connection opened in _app.js");
      setWebsocket(ws);
    };

    return () => {
      if (websocket && websocket.readyState === WebSocket.OPEN) {
        websocket.close();
      }
    };
  }, []);

  if (!websocket) {
    return <div>Loading...</div>;
  }

  return <Home {...pageProps} websocket={websocket} />;
}

export default MyApp;

---

> so how does _app.js import 'bootstrap/dist/css/bootstrap.min.css';
import '../styles/globals.css';
import { useState, useEffect } from 'react';
import Home from './index';

function MyApp({ Component, pageProps }) {
  const [websocket, setWebsocket] = useState(null);

  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8080');

    ws.onopen = () => {
      console.log("WebSocket connection opened in _app.js");
      setWebsocket(ws);
    };

    return () => {
      if (websocket && websocket.readyState === WebSocket.OPEN) {
        websocket.close();
      }
    };
  }, []);

  if (!websocket) {
    return <div>Loading...</div>;
  }

  return <Home {...pageProps} websocket={websocket} />;
}

export default MyApp;

Lead to index.js and make sure to send the socket as a prop?

---

> where should iswebsocketopen be set to true? In app.js? 
import 'bootstrap/dist/css/bootstrap.min.css';
import '../styles/globals.css';
import { useState, useEffect } from 'react';
import Home from './index';

function MyApp({ Component, pageProps }) {
  const [websocket, setWebsocket] = useState(null);

  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8080');

    ws.onopen = () => {
      console.log("WebSocket connection opened in _app.js");
      setWebsocket(ws);
    };

    return () => {
      if (websocket && websocket.readyState === WebSocket.OPEN) {
        websocket.close();
      }
    };
  }, []);

  if (!websocket) {
    return <div>Loading...</div>;
  }

  return <Home {...pageProps} websocket={websocket} />;
}

export default MyApp;

---

## 📝 OpenAI agent for Parliament.
**Date**: 2023-05-09 | **Source**: chatgpt

> Traceback (most recent call last):
  File "/Users/bilalghalib/Projects/scripts/Parliment/parliament-chat-nextjs/pages/parliament_backend/server.py", line 1, in <module>
    parliament = Parliament("Test Parliament")
NameError: name 'Parliament' is not defined

---

> issues? Periodic agent message check
Test Parliament
{'doctor nonfat': <parliament.Agent object at 0x1093b2bc0>}
Task exception was never retrieved
future: <Task finished name='Task-23' coro=<periodic_agent_message_check() done, defined at /Users/bilalghalib/Projects/scripts/Parliment/parliament-chat-nextjs/pages/parliament_backend/server.py:15> exception=AttributeError("'str' object has no attribute 'name'")>
Traceback (most recent call last):
  File "/Users/bilalghalib/Projects/scripts/Parliment/parliament-chat-nextjs/pages/parliament_backend/server.py", line 27, in periodic_agent_message_check
    print(agent.name)
AttributeError: 'str' object has no attribute 'name'
Periodic agent message check
Test Parliament
{'doctor nonfat': <parliament.Agent object at 0x1093b2bc0>}
Task exception was never retrieved
future: <Task finished name='Task-24' coro=<periodic_agent_message_check() done, defined at /Users/bilalghalib/Projects/scripts/Parliment/parliament-chat-nextjs/pages/parliament_backend/server.py:15> exception=AttributeError("'str' object has no attribute 'name'")>

---

## 📝 "Fixing Scope Error"
**Date**: 2023-05-09 | **Source**: chatgpt

> Don't think that's the problem, you see this is the full json message:
 {'action': 'receive_message', 'message': 'assistant says: Sure, here are some general recommendations for taking methyl blue as a liquid:\n\n1. Consult with a healthcare professional: As I mentioned earlier, it is important to consult with a healthcare professional before taking methyl blue or any other supplement. They can help determine if it is safe for you to take and provide guidance on dosing and potential side effects.\n\n2. Start with a low dose: As with any supplement, it is recommended to start with a low dose and gradually increase it over time. A typical starting dose is 1-2 mg per day.\n\n3. Dilute the methyl blue: Since you have a 1% concentration of methyl blue, you will need to dilute it before taking it. A common dilution is 1 mL', 'sender': 'assistant'}

I can change it so it doesn't have "assistant says: "

by changing this

    def get_agent_message(self, agent, chat_history) -> str:
        message = ""
        if agent.agent_type in self.agent_types:
            agent_instance = agent.agent_instance
            if isinstance(agent_instance, self.agent_types[agent.agent_type]):
                response = agent_instance.get_response(chat_history)
                message = f"{agent.name} says: {response}"
        return message
in parliament.py to:


    def get_agent_message(self, agent, chat_history) -> str:
        message = ""
        if agent.agent_type in self.agent_types:
            agent_instance = agent.agent_instance
            if isinstance(agent_instance, self.agent_types[agent.agent_type]):
                response = agent_instance.get_response(chat_history)
                message = f"{response}"
        return message

What else could the problem be?

---

> after adding all those debugs here's my terminal, where is the message not showing up:
{'action': 'receive_message', 'message': 'testing', 'sender': 'assistant'} responsetest sent
data {'action': 'send_message', 'sender': 'ment', 'message': 'We got this yall'}
Received message: We got this yall
Broadcasting message: We got this yall
assistant's speaking pressure: 1
assistant started speaking task
{'action': 'receive_message', 'message': 'testing', 'sender': 'assistant'} responsetest sent
Broadcasting message: Great! Is there anything specific you need help with or any questions you have?
assistant's speaking pressure: 2
Agent message: Great! Is there anything specific you need help with or any questions you have?
Sending response: {'action': 'receive_message', 'message': 'Great! Is there anything specific you need help with or any questions you have?', 'sender': 'assistant'}
assistant started speaking task
{'action': 'receive_message', 'message': 'testing', 'sender': 'assistant'} responsetest sent
assistant started speaking task
{'action': 'receive_message', 'message': 'testing', 'sender': 'assistant'} responsetest sent

---

## 📝 Agent Pressure Buildup.
**Date**: 2023-05-08 | **Source**: chatgpt

> Periodic agent message check
Task exception was never retrieved
future: <Task finished name='Task-10' coro=<periodic_agent_message_check() done, defined at /Users/bilalghalib/Projects/scripts/Parliment/parliament-chat-nextjs/pages/parliament_backend/server.py:60> exception=TypeError("get_agent_message() missing 1 required positional argument: 'agent'")>
Traceback (most recent call last):
  File "/Users/bilalghalib/Projects/scripts/Parliment/parliament-chat-nextjs/pages/parliament_backend/server.py", line 64, in periodic_agent_message_check
    agent_message = parliament.get_agent_message()
TypeError: get_agent_message() missing 1 required positional argument: 'agent'
Periodic agent message check
Periodic agent message check
Task exception was never retrieved
future: <Task finished name='Task-15' coro=<periodic_agent_message_check() done, defined at /Users/bilalghalib/Projects/scripts/Parliment/parliament-chat-nextjs/pages/parliament_backend/server.py:60> exception=TypeError("get_agent_message() missing 1 required positional argument: 'agent'")>
Traceback (most recent call last):
  File "/Users/bilalghalib/Projects/scripts/Parliment/parliament-chat-nextjs/pages/parliament_backend/server.py", line 64, in periodic_agent_message_check
    agent_message = parliament.get_agent_message()
TypeError: get_agent_message() missing 1 required positional argument: 'agent'
Periodic agent message check

---

> Parliament.js already has an add agent def:

    def add_agent(self, name: str, speaking_pressure_threshold: int, context: str):
        self.agents.append({
            "name": name,
            "speaking_pressure_threshold": speaking_pressure_threshold,
            "context": context,
            "speaking_pressure": 0,
            "agent_type": "default"  # Add a default agent type
        })

---

> Parliament.py already has an add agent def:

    def add_agent(self, name: str, speaking_pressure_threshold: int, context: str):
        self.agents.append({
            "name": name,
            "speaking_pressure_threshold": speaking_pressure_threshold,
            "context": context,
            "speaking_pressure": 0,
            "agent_type": "default"  # Add a default agent type
        })

---

> like this?
For settings.js:
import { useState } from 'react';
import { Button, Form, Table } from 'react-bootstrap';

function Settings({ onStartParliament, props }) {
  const websocket = props.websocket;
  const [parliamentName, setParliamentName] = useState('');
  const [topic, setTopic] = useState('');
For _app.js

import 'bootstrap/dist/css/bootstrap.min.css';
import '../styles/globals.css';
import { useState, useEffect } from 'react';

function MyApp({ Component, pageProps }) {
  const [websocket, setWebsocket] = useState(null);

  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8080');
    setWebsocket(ws);
    return () => {
      ws.close();
    };
  }, []);

  if (!websocket) {
    return <div>Loading...</div>;
  }
  <Settings onStartParliament={...} websocket={props.websocket} />

  return <Component {...pageProps} websocket={websocket} />;
}

export default MyApp;
(I'm not sure I did _app.js right)

---

> I like this process of putting it into the agent class and I want to have a different increment for every agent and instead of triggering at a specific increment I want it to trigger when speaking pressure is 100 it triggers the moment to speak and that each agent has an increment every time increment_pressure goes, either each 15 seconds or when the user sends a new message

---

> parliament.add_agent(agent_type, agent_name, "100", context, pressure_increment, websocket)


class Agent:
    def __init__(self, name: str, speaking_pressure_increment: int, context: str, agent_type: str, parliament, pressure_increment: int, agent_instance=None, websocket=None):
        self.name = name
        self.speaking_pressure_increment = speaking_pressure_increment
        self.context = context
        self.speaking_pressure = 0
        self.pressure_increment = pressure_increment
        self.agent_type = agent_type
        self.agent_instance = agent_instance
        self.speaking_event = asyncio.Event()
        self.parliament = parliament
        self.websocket = websocket
        asyncio.create_task(self.increment_pressure())  # start the increment_pressure() method as a background task

---

> This is the implementation:    def get_time_since_user_spoke(chat_history):
        # Reverse the chat history so we start from the latest messages
        reversed_chat_history = reversed(chat_history)
        for message_data in reversed_chat_history:
            if message_data['sender'] == 'user':
                # Get the timestamp of the last user message
                last_user_message_time = message_data['timestamp']
                # Get the current time
                current_time = datetime.now()
                # Calculate the time difference in seconds
                time_difference = (current_time - last_user_message_time).total_seconds()
                return time_difference
        return None  # Return None if the user has never spoken

---

> what about only adding the person at the top of the list rather than the whole list? and making the person at the head of the line also have a speaking pressure of 100% and then add anyone else in the line that also has a speaking pressure of 100% next in line, as well as anyone tagged
So relevancy sorted pick the top person, give them a speaking pressure of a hundred percent and put them in the queue, then add to the queue if anyone has been tagged. Maybe we should add a variable (tagged) so that we can pick them out easier and then mark them as untagged when they respond. Lastly we see if anyone else has over 100% speaking pressure, add them next to the queue

---

> Do I need ?        def get_agent_message(self, agent, chat_history) -> str:
            message = ""
            if agent.agent_type in self.agent_types:
                agent_instance = agent.agent_instance
                if isinstance(agent_instance, self.agent_types[agent.agent_type]):
                    response = agent_instance.get_response(chat_history)
                    message = f"{response}"
            return message

---

## 📝 Bootstrap Install Error.
**Date**: 2023-05-08 | **Source**: chatgpt

> ./pages/index.js:2:0
Module not found: Can't resolve '../components/Settings'
  1 | import { useState } from 'react';
> 2 | import Settings from '../components/Settings';
  3 | import Chat from '../components/Chat';
  4 | 
  5 | export default function Home() {

https://nextjs.org/docs/messages/module-not-found
This error occurred during the build process and can only be dismissed by fixing the error.

---

> ./pages/components/Chat.js:2:0
Module not found: Can't resolve 'react-bootstrap'
  1 | import { useState, useEffect } from 'react';
> 2 | import { Button, Form } from 'react-bootstrap';
  3 | 
  4 | function Chat({ parliament }) {
  5 |   const [messages, setMessages] = useState([]);

https://nextjs.org/docs/messages/module-not-found

Import trace for requested module:
./pages/index.js

---

## 📝 Create AI Parliamentarians.
**Date**: 2023-05-08 | **Source**: chatgpt

> It should rather than immediately create all agents add them one at a time to the add agents rows and then allow the user to click the startParliment button rather than doing it all at once. 
Make a drop down selector that says select preset and have one of the presets be "six thinking hats" when that's selected it should repopulate six rows of agents with the information and the user should be able to edit them or click start parliament.

---

## 📝 Create Parliament API.
**Date**: 2023-05-07 | **Source**: chatgpt

> update this get_agent_message with what's needed:

    def get_agent_message(self) -> str:
        # Find the agent with the highest speaking_pressure
        agent = max(self.agents, key=lambda x: x["speaking_pressure"])
        agent["speaking_pressure"] = 0

        # Generate agent message
        message = f"{agent['name']} says: "

        for plugin in self.plugins:
            plugin_output = plugin.process(agent["context"])
            if plugin_output:
                message += plugin_output

        return message

---

## 📝 Team Well-being Assessment.
**Date**: 2023-05-05 | **Source**: chatgpt

> Can you make it more quantitative and less subjective how can we assess this with measures and benchmarks. I don't want subjective answers like "on a scale of 1-10 how much do you believe that..." I prefer things like "my heart rate variability is above average for someone my age" and similar actual measures, if it's not possible perhaps we can assess "other people tell me that I'm a very cheerful person" to get somewhat more externally verifiable information.

---

## 📝 Auto-GPT Package Error
**Date**: 2023-05-04 | **Source**: chatgpt

> ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.
conda-repo-cli 1.0.4 requires pathlib, which is not installed.
anaconda-project 0.10.2 requires ruamel-yaml, which is not installed.

---

## 📝 Ruby & CocoaPods Setup.
**Date**: 2023-04-28 | **Source**: chatgpt

> it says I shouldn't use external ways to update the ruby on a Mac because it might break things maybe I shouldn't?
Pruned 0 symbolic links and 12 directories from /opt/homebrew
==> Caveats
==> ruby
ruby is keg-only, which means it was not symlinked into /opt/homebrew,
because macOS already provides this software and installing another version in
parallel can cause all kinds of trouble.

If you need to have ruby first in your PATH, run:
  echo 'export PATH="/opt/homebrew/opt/ruby/bin:$PATH"' >> ~/.zshrc

---

## 📝 Server shutdown error.
**Date**: 2023-04-27 | **Source**: chatgpt

> how do I kill these? ^C
root@tender-mendel:/var/discourse# sudo netstat -plnt | grep 443.
tcp        0      0 10.18.0.7:443           0.0.0.0:*               LISTEN      10696/nginx: master 
tcp        0      0 128.199.53.128:443      0.0.0.0:*               LISTEN      10696/nginx: master 
tcp        0      0 0.0.0.0:8443            0.0.0.0:*               LISTEN      1165/sw-cp-server:  
tcp6       0      0 2a03:b0c0:2:d0::d29:443 :::*                    LISTEN      10696/nginx: master 
tcp6       0      0 :::8443                 :::*                    LISTEN      1165/sw-cp-server:  
root@tender-mendel:/var/discourse# kill ps 10696

---

## 📝 Chicago Deaf Refugee Sponsors.
**Date**: 2023-04-26 | **Source**: chatgpt

> I want to find 5 corporate sponsors in the Chicago area that may be interested in supporting a deaf refugee nonprofit 501c3 organization, can you help

---

## 📝 New chat
**Date**: 2023-04-19 | **Source**: chatgpt

> bg@bilalghalib.com
I’m about to have a child and I want to Interview my dad, what is a good interview structure and timeline and process and what are good questions? Critique your work when done

---

## 📝 Pantheon Synonyms.
**Date**: 2023-04-18 | **Source**: chatgpt

> Can you remove the idea of greek culture and come up with 10 similarly cute ideas for names that relate to group wisdom, what angle might make sense - I was thinking it would be neat to use debono's six thinking hats as a first prototype where you create 6 different personas that represent different styles of thinking that can help you refine your ideas

---

## 📝 Docker daemon not running.
**Date**: 2023-04-13 | **Source**: chatgpt

> DEPRECATED: The legacy builder is deprecated and will be removed in a future release.
            Install the buildx component to build images with BuildKit:
            https://docs.docker.com/go/buildx/

Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?
docker: Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?.
See 'docker run --help'.

---

> ./setup.sh: line 15: .env: Permission denied
./setup.sh: line 18: .env.docker: Permission denied
DEPRECATED: The legacy builder is deprecated and will be removed in a future release.
            Install the buildx component to build images with BuildKit:
            https://docs.docker.com/go/buildx/

Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?
docker: Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?.
See 'docker run --help'.

---

## 📝 Port already in use.
**Date**: 2023-04-09 | **Source**: chatgpt

> yeah, it somehow restarts when discourse is trying to rebuild and then it covers the port so I want to turn it off start up discourse and then turn it on if needed

---

## 📝 Taddei Interview: Education & Innovation
**Date**: 2023-03-31 | **Source**: chatgpt

> I am going to interview Francois taddei today for a podcast, what should I keep in mind, what questions might I ask that would evoke his depth and interests? should it be a discussion or should I listen more? give me an instruction set as a one pager of notes that I can print to take to the interview to keep in mind

---

## 📝 Yarn Compatibility Error.
**Date**: 2023-03-29 | **Source**: chatgpt

> WARNING: The legacy expo-cli does not support Node +17. Migrate to the versioned Expo CLI (npx expo).
Warning! Your git working tree is dirty.
It's recommended to commit all your changes before proceeding, so you can revert the changes made by this command if necessary.

? Would you like to proceed? › (Y/n)

---

## 📝 Socratic Method For Tensors.
**Date**: 2023-03-27 | **Source**: chatgpt

> I don’t know how to make a valid tensor let’s say I wanted to pick a bunch of numbers to make a tensor 1 2 3 on the first row 2 4 5 on the second row 6 7 9 on the third row for the matrix one and then a matrix to 2 4 8 on the first row 3 1 3 on the second row and 5 1 0 on the last row is that tensor and why not

---

## 📝 Animate Islamic Prayer Times.
**Date**: 2023-03-25 | **Source**: chatgpt

> Ok, then use this externally generated athan times:
remember the circle should be split into the five segments representing the times with the names as well:
{'Fajr': '05:15', 'Sunrise': '06:44', 'Dhuhr': '12:57', 'Asr': '16:22', 'Sunset': '19:10', 'Maghrib': '19:10', 'Isha': '20:39', 'Imsak': '05:05', 'Midnight': '00:57', 'Firstthird': '23:02', 'Lastthird': '02:53', 'date': {'readable': '25 Mar 2023', 'timestamp': '1679724000', 'hijri': {'date': '03-09-1444', 'format': 'DD-MM-YYYY', 'day': '03', 'weekday': {'en': 'Al Sabt', 'ar': 'السبت'}, 'month': {'number': 9, 'en': 'Ramaḍān', 'ar': 'رَمَضان'}, 'year': '1444', 'designation': {'abbreviated': 'AH', 'expanded': 'Anno Hegirae'}, 'holidays': []}, 'gregorian': {'date': '25-03-2023', 'format': 'DD-MM-YYYY', 'day': '25', 'weekday': {'en': 'Saturday'}, 'month': {'number': 3, 'en': 'March'}, 'year': '2023', 'designation': {'abbreviated': 'AD', 'expanded': 'Anno Domini'}}}}

---

> error: AttributeError: 'NoneType' object has no attribute 'deg2rad'

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/Users/bilalghalib/opt/anaconda3/lib/python3.9/site-packages/matplotlib/cbook/__init__.py", line 287, in process
    func(*args, **kwargs)
  File "/Users/bilalghalib/opt/anaconda3/lib/python3.9/site-packages/matplotlib/animation.py", line 909, in _start
    self._init_draw()
  File "/Users/bilalghalib/opt/anaconda3/lib/python3.9/site-packages/matplotlib/animation.py", line 1698, in _init_draw
    self._draw_frame(frame_data)
  File "/Users/bilalghalib/opt/anaconda3/lib/python3.9/site-packages/matplotlib/animation.py", line 1720, in _draw_frame
    self._drawn_artists = self._func(framedata, *self._args)
  File "<stdin>", line 6, in update_circle
TypeError: loop of ufunc does not support argument 0 of type NoneType which has no callable deg2rad method
>>>

---

## 📝 Body Composition Summary.
**Date**: 2023-03-25 | **Source**: chatgpt

> Month,Overall,,,,,,,,,,,,,,,,,,,,,,,Right-Leg,,,,Left-Leg,,,,Right-Hand,,,,Left-Hand,,,,Core,,,
,Height,Weight KG,BMI,Fat KG,Fat %,Fat-Free KG,internal lubrication degree,total Liquid KG,total Liquid %, in-cell Liquid,out-cell liquid ,Muscel KG,Bone Weight KG,Protein KG,Proten %,Minral KG,BMH KCal,Metabolism age,Body Density,obesity Dgree,Ideal-Weight,Ideal-Fat,Ideal-Liquid,Fat %,Fat KG,Fat-Free KG,Muscel KG,Fat %,Fat KG,Fat-Free KG,Muscel KG,Fat %,Fat KG,Fat-Free KG,Muscel KG,Fat %,Fat KG,Fat-Free KG,Muscel KG,Fat %,Fat KG,Fat-Free KG,Muscel KG
Sara_14-Nov-22,150,62.5,27.8,22.7,36.4,39.8,5,31,48.8,17,14,37.7,2,6.39,10.224,2.91,1264,33,1.0142,23.44,45-65,18-26,50-61,41.4,4.46,6.32,6,40.8,4.43,6.42,6.1,38.6,1.26,2,1.9,41.3,1.33,1.9,1.8,32.7,11.26,23.17,22
Sara_Dec,150,63.3,28.2,22.8,36,40.5,5,31,49.29,17,14,38.4,2.1,6.34,10.016,2.96,1283,33,1.0151,25.02,45-65,18-26,50-61,41.9,4.64,6.43,6.1,41.3,4.6,6.54,6.2,38.6,1.26,2,1.9,40.2,1.28,1.9,1.8,31.8,11.06,23.73,22.5
Sara_12_Jan_23,150,63,28,21.2,33.7,41.8,4,32,50.16,18,14,39.7,2.1,7.15,11.349,3.05,1310,33,1.0203,24.43,45-65,18-26,50-61,41,4.45,6.53,6.2,40.3,4.48,6.63,6.3,36.2,1.19,2.11,2,38.8,1.27,2,1.9,28.3,9.64,24.43,23.2
Sara_12_Feb_23,150,63,28,22.6,35.8,40.5,5,31,49.68,17,14,38.4,2.1,6.24,9.905,2.96,1281,33,1.0156,24.43,45-65,18-26,50-61,42.1,4.6,6.33,6,41.6,4.58,6.43,6.1,37.7,1.21,2,1.9,39.4,1.3,2,1.9,31.4,10.81,23.63,22.4
Sara_18_Mar_23,150,63.4,28.2,22.2,35,41.2,5,31,49.53,17,14,39.1,2.1,6.79,10.710,3.01,1295,34,1.0174,25.22,45-65,18-26,50-61,42.2,4.69,6.43,6.1,41.3,4.6,6.53,6.2,37.3,1.25,2.11,2,38.2,1.3,2.11,2,30.1,10.39,24.13,22.9

---

> here also mohammed measurements
can you provide a similar workout for him based on his data

Month,Overall,,,,,,,,,,,,,,,,,,,,,,,Right-Leg,,,,Left-Leg,,,,Right-Hand,,,,Left-Hand,,,,Core,,,
,Height,Weight KG,BMI,Fat KG,Fat %,Fat-Free KG,internal lubrication degree,total Liquid KG,total Liquid %, in-cell Liquid,out-cell liquid ,Muscel KG,Bone Weight KG,Protein KG,Proten %,Minral KG,BMH KCal,Metabolism age,Body Density,obesity Dgree,Ideal-Weight,Ideal-Fat,Ideal-Liquid,Fat %,Fat KG,Fat-Free KG,Muscel KG,Fat %,Fat KG,Fat-Free KG,Muscel KG,Fat %,Fat KG,Fat-Free KG,Muscel KG,Fat %,Fat KG,Fat-Free KG,Muscel KG,Fat %,Fat KG,Fat-Free KG,Muscel KG
Mo_12-Nov-22,182,83.9,25.3,22.2,26.5,61.7,7,45,53.16,26,19,58.6,3.1,12.6,15.018,4.5,1849,30,1.037,12.57,66-82,10-20,55-66,20.6,2.73,10.53,10,21.7,2.86,10.32,9.8,23.5,1.1,3.85,3.4,23.6,1.11,3.85,3.4,30,14.48,33.8,32.1
Mo_12-Dec-22,182,84.3,25.4,22.4,26.5,61.9,7,44,52.31,26,18,58.8,3.1,13.28,15.753,4.52,1857,30,1.037,13.11,66-82,10-20,55-66,21.5,2.85,10.42,9.9,22.2,2.91,10.21,9.7,23.5,1.07,3.47,3.3,22.4,1.03,3.58,3.4,29.8,14.52,34.21,32.5
Mo_12_Jan_23,182,85.2,25.7,22.3,26.1,62.9,7,45,52.46,27,18,59.8,3.1,13.61,15.974,4.59,1885,30,1.038,14.32,66-82,10-20,55-66,20.1,2.7,10.73,10.2,21.2,2.8,10.41,9.9,22.9,1.06,3.58,3.4,22.8,1.06,3.58,3.4,29.7,14.62,34.61,32.9
Mo_12_Feb_23,182,84.5,25.5,22.5,26.6,62,7,44,52.54,26,18,58.9,3.1,13.07,15.467,4.53,1860,30,1.0368,13.38,66-82,10-20,55-66,20.6,2.73,10.53,10,21.6,2.84,10.32,9.8,23.8,1.08,3.47,3.3,23.2,1.08,3.58,3.4,30.2,14.8,34.21,32.5
Mo_18_Mar_23,182,84.8,25.6,22.8,26.9,62,7,45,52.59,26,19,58.9,3.1,12.87,15.177,4.53,1861,30,1.036,13.78,66-82,10-20,55-66,20.6,2.73,10.53,10,21.6,2.84,10.32,9.8,23.9,1.09,3.47,3.3,23.2,1.08,3.58,3.4,30.6,15.04,34.11,32.4

---

## 📝 SEO tags for Petrichor Oil.
**Date**: 2023-03-22 | **Source**: chatgpt

> merging with this Orange Blossom Essential Oil, Neroli, Sweet Orange Essential Oil, Organic Essential Oil, Aromatherapy Essential Oil, Therapeutic Grade Oil
Give me 10 options and a reasoning behind all keywords with data indicating why it would be good for SEO based on search data you can find from 2021

---

## 📝 Explore Emotions Deeply.
**Date**: 2023-03-01 | **Source**: chatgpt

> I'm having difficulty connecting with my emotions and I'm not sure why. I'm wondering if you can help me explore this further. Sometimes I worry that I might be on the spectrum, but I'm not sure. Can you guide me through some questions or exercises that might help me understand why I'm having difficulty with my emotions?

---

> sounds good, probably best to have a practitioner because if she knows that I may have partially picked her because she's easy to avoid it would make her very sad. can you ask me a few questions to determine if it's true that I chose her to simplify avoidance or if this is just a self destructive line of thought

---

> I initially felt a quiet yes inside of me when I hugged her. I didn't feel a lot of sexual attraction or intellectual attraction. it was a quiet calming of my body that I thought was an intuition that she was right. and moreover she was chosen by god. I was practicing being quiet and listening within. now I regret that sometimes because I wish I was super attracted and stimulated in more ways and instead I have a 8 year old memory of a quiet calm moment in my body. I do have a strange commitment addiction though. I love thinking of the right thing to do philosophically and theoretically and sticking to things. makes me proud of myself I guess... I'm sure there's something here, what do you think?

---

> interesting, ok, why didn't you answer when I put them in this format:, what's the mean median and mode of the seconds between my post times 
and instead only answered when I asked each one at a time. I want to know so I can ask better questions

---

> how can I develop these things at work? I work as a co-founder in a business and it takes up a LOT of my time - I sit at a computer all day. I've always been a nerdy computer person except I never really was able to get into the depth of the maths, I always wanted things to work fast. It's sad, I wish I was a better nerd

---

> what are the reasons, think creatively and outside the box, that adhd might be improved by physical activities?

---

> can you make a chart comparing these with a column that describes behaviors and another of symptoms that are giveaways for that type? personality disorders, including borderline personality disorder, narcissistic personality disorder, histrionic personality disorder, and antisocial personality disorder, among others.

---

> continue after this segment: "			<node CREATED="2023-03-10 18:36:07.058" ID="ID_1635260767057" MODIFIED="2023-03-10 18:36:07.058" TEXT="Self-Talk"/>
			<node CREATED="2023-03-10 18:36:24.556" ID="ID_1635260784555" MODIFIED="2023-03-10 18:36:24.556" TEXT="Mindfulness"/>
			<node CREATED="2023-03-10 18:37:02.372" ID="ID_1635260822371" MODIFIED="2023-03-10 18:37:02.372" TEXT="Gratitude"/>
"

---

