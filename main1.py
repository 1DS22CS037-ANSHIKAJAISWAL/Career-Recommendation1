import streamlit as st
import requests
from datetime import datetime


# Define the API functions (as shown above)

def fetch_linkedin_opportunities(specific_interest, location=""):
    api_key = "YOUR_LINKEDIN_API_KEY"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    url = f"https://api.linkedin.com/v2/jobSearch?q={specific_interest}&location={location}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        opportunities = []
        for job in data["elements"]:
            opportunity = {
                "title": job.get("title"),
                "company": job.get("companyName"),
                "location": job.get("location"),
                "link": job.get("link")
            }
            opportunities.append(opportunity)
        return opportunities
    else:
        return []


def fetch_eventbrite_events(specific_interest, location=""):
    api_key = "YOUR_EVENTBRITE_API_KEY"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    url = f"https://www.eventbriteapi.com/v3/events/search/?q={specific_interest}&location.address={location}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        events = []
        for event in data["events"]:
            event_info = {
                "name": event["name"]["text"],
                "date": event["start"]["local"],
                "location": event.get("venue", {}).get("address", {}).get("localized_address_display"),
                "link": event["url"]
            }
            events.append(event_info)
        return events
    else:
        return []


def fetch_coursera_courses(specific_interest):
    url = f"https://api.coursera.org/api/courses.v1?q=search&query={specific_interest}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        courses = []
        for course in data["elements"]:
            course_info = {
                "title": course["name"],
                "provider": "Coursera",
                "link": f"https://www.coursera.org/learn/{course['slug']}"
            }
            courses.append(course_info)
        return courses
    else:
        return []


def main():
    st.title("Career Guidance and Opportunities")

    st.header("Student Information")

    # Step 1: Ask for student's general interest
    interest = st.selectbox(
        "What is your primary field of interest?",
        ["Engineering", "Medicine", "Arts", "Business", "Science", "Technology"]
    )

    # Step 2: Ask for more specific interest based on the general interest
    specific_interest = ""
    if interest == "Engineering":
        specific_interest = st.selectbox(
            "Which field of engineering are you interested in?",
            ["Mechanical Engineering", "Civil Engineering", "Electrical Engineering", "Computer Engineering",
             "Chemical Engineering"]
        )
    elif interest == "Medicine":
        specific_interest = st.selectbox(
            "Which field of medicine are you interested in?",
            ["General Medicine", "Surgery", "Dentistry", "Pharmacy", "Nursing"]
        )
    elif interest == "Arts":
        specific_interest = st.selectbox(
            "Which field of arts are you interested in?",
            ["Literature", "Performing Arts", "Visual Arts", "History", "Languages"]
        )
    elif interest == "Business":
        specific_interest = st.selectbox(
            "Which field of business are you interested in?",
            ["Finance", "Marketing", "Human Resources", "Entrepreneurship", "Management"]
        )
    elif interest == "Science":
        specific_interest = st.selectbox(
            "Which field of science are you interested in?",
            ["Biology", "Chemistry", "Physics", "Environmental Science", "Mathematics"]
        )
    elif interest == "Technology":
        specific_interest = st.selectbox(
            "Which field of technology are you interested in?",
            ["Information Technology", "Data Science", "Cybersecurity", "Artificial Intelligence",
             "Software Development"]
        )

    # Step 3: Ask for student's skill sets, achievements, certifications, education level, and internships
    st.subheader("Please provide more details about yourself")

    skills = st.text_area("List your skills (comma separated):")
    achievements = st.text_area("List your achievements (comma separated):")
    certifications = st.text_area("List your certifications (comma separated):")
    education_level = st.selectbox(
        "What is your current education level?",
        ["High School", "Undergraduate", "Postgraduate", "Doctorate"]
    )
    internships = st.number_input("Number of internships done:", min_value=0, step=1)

    # Step 4: Recommend career guidance, competitions, and opportunities based on the provided information
    if st.button("Get Recommendations"):
        st.subheader("Recommendations")

        # Fetch opportunities from LinkedIn
        linkedin_opportunities = fetch_linkedin_opportunities(specific_interest)
        st.write("### Job and Internship Opportunities:")
        for opportunity in linkedin_opportunities:
            st.write(
                f"- [{opportunity['title']} at {opportunity['company']}]({opportunity['link']}) - {opportunity['location']}")

        # Fetch events from Eventbrite
        eventbrite_events = fetch_eventbrite_events(specific_interest)
        st.write("### Competitions and Events:")
        for event in eventbrite_events:
            st.write(f"- [{event['name']}]({event['link']}) - {event['date']} - {event['location']}")

        # Fetch courses from Coursera
        coursera_courses = fetch_coursera_courses(specific_interest)
        st.write("### Recommended Courses:")
        for course in coursera_courses:
            st.write(f"- [{course['title']}]({course['link']}) - {course['provider']}")


if __name__ == "__main__":
    main()
