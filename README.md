# CMADeveloperCodeTest

## Install Directions
***
pip install -r requirements.txt
***

## Execution Directions
***
To run, enter - python main.py
***

## Documentation

> How did you approach this problem and why you end up with the solution you did?

I looked briefly at the online listing of exhibitions, but decided I wanted to do something a bit more data driven. To narrow into the 1916 Exhibition, I wanted to use two types of filtering, string and date, to illustrate multiple ways at arriving at the goal within this sort of API/Dataset. From there, I wanted to make use of another endpoint and use information in the schema which was not directly queryable, number of exhibitions, while using a built-in function, len. I allowed the length of this query to be fairly cumbersome to recreate a simple data mining workflow which could be augmented with more parameters or scope depending on project needs. I hadn't actually picked out my "Highlight" artwork before this process and noticing that its record had been recently updated was a fun coincidence. From there, I grabbed others which had been recently updated, the relation between them became obvious and I felt that was a nice conclusion to the exercise. 

> How long did it take you to complete?

I spent a few hours with the code. It was my first time working with the Open Access API and I was having fun exploring some options. Once I got the core functions working properly, I wanted to take some time making the terminal output readable and step-by-step, and ensuring consistent formatting.

> How would you change your solution in order to scale it up to a web application where users can select an exhibition, highlight and similarity criteria, and receive results?

The reliance on the opening_date parameter could easily be modified to accept inputs for different date ranges - say specific months or themes throughout the year. Or it could be interesting to look at the longest or shortest exhibitions by comparing against the spans between opening and closing dates.

> How would you set this up as a process that runs daily, with different results, and posts them to social media platforms via API?

I haven't worked directly with social sites through APIs, but since the results of this work can be best expressed through images of artworks, I would likely first look to Instagram's Graph API as a destination. While posting the most recently updated records would be a nice way to highlight the on-going work of museum staff behind the scenes, there would certainly be days during which records had not been updated. What would likely be more consistent would be to look at a parameter like athena_id and parse the int in a way which could be matched against the current date. This would not necessarily be significant against the date but could ensure some degree of randomness and draw from the most available field in the API to ensure continued posts.
