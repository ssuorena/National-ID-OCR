import streamlit as st
import requests
from matplotlib import pyplot as plt
from PIL import Image
import numpy as np

import streamlit.components.v1 as components

# Read the HTML file
with open('Analytic.html', 'r') as file:
    html_code = file.read()

# Embed the HTML code in the Streamlit app
components.html(html_code)

# API endpoint
url = 'http://127.0.0.1:8000/api/upload/'
portre = False



st.title('National ID Card OCR')


st.divider()
st.write('Please take a picture from yor national ID card and upload it...')
st.image('Static Images/ID_card.PNG',width=200,caption='ID card image style')


Upload, Camera = st.columns(2)
# Upload image file
uploaded_file = Upload.file_uploader("Choose an ID card image...", type=["jpg", "jpeg", "png"])
print(uploaded_file)

img_file_buffer = Camera.camera_input("Take a picture from your id card")


if (uploaded_file is not None) or (img_file_buffer is not None):
    if uploaded_file is not None:
        files = {'image': uploaded_file}
        st.divider()
        with st.spinner('Analysing your ID card...'):
            try:
                response = requests.post(url, files=files,timeout=100)
                # Check if the request was successful
                if response.status_code == 200:
                    col1, col2 = st.columns(2)
                    st.success('Analysing is done!', icon="✅")
                    Data = response.json()
                    if 'Info' in Data:
                        data = Data['Info']
                    else:
                        data = {}
                    if 'Prtrate' in Data:    
                        portrate = Data['Prtrate']
                        portre = True

                    col2.markdown(
                        """
                    <style>
                    [data-testid="stMetricValue"] {
                        font-size: 30px;
                    }
                    </style>
                    """,
                        unsafe_allow_html=True,
                    )
                    if 'Name' in data:
                        col2.metric(label="نام", value=data['Name'])
                        
                    if 'Family Name' in data:
                        col2.metric(label="نام خانوادگی", value=data['Family Name'])
                        
                    if "Father's Name" in data:
                        col2.metric(label="نام پدر", value=data["Father's Name"])
                        
                    if 'ID' in data:
                        col2.metric(label='کد ملی', value=data['ID'])
                        
                    if 'City' in data:
                        col2.metric(label='محل تولد' ,value=data['City'])
                        
                    if 'birsth date_per' in data:
                        col2.metric(label='تاریخ تولد', value=data['birsth date_per'])
                        
                    if 'Gender' in data:
                        if data['Gender']=='man':
                            gen ='مرد'
                        else:
                            gen ='زن'
                        col2.metric(label='جنسیت', value=gen)
                        
                    if portre:
                        plt.imshow(portrate)
                        plt.axis('off')
                        portrate_path = 'saved_figure.png'
                        plt.savefig(portrate_path)
                        col1.image(portrate_path, caption='آواتار استخراج شده از کارت ملی')
                    
                    
                    
                else:
                    error = 'Failed to upload image:'+ str(response.status_code) + str(response.text)
                    st.error('This is an error:'+'\n'+error, icon="🚨")
            except requests.RequestException as e:
                st.error('This is an error with server:'+'\n'+str(e), icon="🚨")
                


    if img_file_buffer is not None:

        img = Image.open(img_file_buffer)
        files = {'image': img}
        st.divider()
        # Send a POST request
        with st.spinner('Analysing your ID card...'):
            try:
                response = requests.post(url, files=files,timeout=100)
                # Check if the request was successful
                if response.status_code == 200:
                    col1, col2 = st.columns(2)
                    st.success('Analysing is done!', icon="✅")
                    Data = response.json()
                    if 'Info' in Data:
                        data = Data['Info']
                    else:
                        data = {}
                    if 'Prtrate' in Data:    
                        portrate = Data['Prtrate']
                        portre = True

                    col2.markdown(
                        """
                    <style>
                    [data-testid="stMetricValue"] {
                        font-size: 30px;
                    }
                    </style>
                    """,
                        unsafe_allow_html=True,
                    )
                    if 'Name' in data:
                        col2.metric(label="نام", value=data['Name'])
                        
                    if 'Family Name' in data:
                        col2.metric(label="نام خانوادگی", value=data['Family Name'])
                        
                    if "Father's Name" in data:
                        col2.metric(label="نام پدر", value=data["Father's Name"])
                        
                    if 'ID' in data:
                        col2.metric(label='کد ملی', value=data['ID'])
                        
                    if 'City' in data:
                        col2.metric(label='محل تولد' ,value=data['City'])
                        
                    if 'birsth date_per' in data:
                        col2.metric(label='تاریخ تولد', value=data['birsth date_per'])
                        
                    if 'Gender' in data:
                        if data['Gender']=='man':
                            gen ='مرد'
                        else:
                            gen ='زن'
                        col2.metric(label='جنسیت', value=gen)
                        
                    if portre:
                        plt.imshow(portrate)
                        plt.axis('off')
                        portrate_path = 'saved_figure.png'
                        plt.savefig(portrate_path)
                        col1.image(portrate_path, caption='آواتار استخراج شده از کارت ملی')
                    
                    
                    
                else:
                    error = 'Failed to upload image:'+ str(response.status_code) + str(response.text)
                    st.error('This is an error:'+'\n'+error, icon="🚨")
            except requests.RequestException as e:
                st.error('This is an error with server:'+'\n'+str(e), icon="🚨")




st.markdown("""
    <script>
    // Define constant parameters:
    const scrollPercentLimit = 80
    const SESSION_TIMEOUT = 1 * 60 * 1000; // 30 minutes in milliseconds
    let sessionId = getSessionId();
    let sessionTimeout;
    let hasTriggered80PercentScroll = false;
    let deviceInfo = null;
    let ip = null;
    let utmParameters = null;

    // Initialize events array from session storage or empty array:
    let eventsArray = JSON.parse(sessionStorage.getItem('eventsArray')) || [];

    // Generate a session ID with a random process:
    function generateSessionId() {
      return 'xxxx-xxxx-4xxx-yxxx-xxxx'.replace(/[xy]/g, function(c) {
        var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
      });
    }

    // Get the current timestamp:
    function getCurrentTimestamp() {
      return new Date().getTime();
    }

    // Retrieve device information:
    function getDeviceInfo() {
      const brand = navigator.userAgentData?.brands?.[0]?.brand || 'unknown';
      const version = navigator.userAgentData?.brands?.[0]?.version || 'unknown';
      const platform = navigator.userAgentData?.platform || 'unknown';
      return { platform: platform, browser_brand: brand, browser_version: version };
    }

    // Retrieve or generate a session ID:
    function getSessionId() {
      let sessionId = sessionStorage.getItem('sessionId');
      let lastActivity = sessionStorage.getItem('lastActivity');
      let currentTime = getCurrentTimestamp();

      if (!sessionId || !lastActivity || (currentTime - lastActivity > SESSION_TIMEOUT)) {
        sessionId = generateSessionId();
        sessionStorage.setItem('sessionId', sessionId);
      }

      sessionStorage.setItem('lastActivity', currentTime);
      
      return sessionId;
    }

    // Get the IP address using an external API:
    async function getIpAddress() {
      try {
        const response = await fetch('https://api.ipify.org?format=json');
        if (!response.ok) throw new Error('Failed to fetch IP address');
        const data = await response.json();
        return data.ip;
      } catch (error) {
        console.error('Error getting IP address:', error);
        return null;
      }
    }

    // Get UTM parameters from the URL:
    function getUTMParameters() {
      const urlParams = new URLSearchParams(window.location.search);
      const utmSource = urlParams.get('utm_source') || 'null';
      const utmMedium = urlParams.get('utm_medium') || 'null';
      return { utmSource, utmMedium };
    }

    // Initialize the data layer:
    window.myDataLayer = window.myDataLayer || [];

    // Track events and push them to the events array:
    async function trackEvent(eventName, eventData) {
      if (!deviceInfo) {
        deviceInfo = getDeviceInfo();
      }
      if (!ip) {
        ip = await getIpAddress();
      }
      if (!utmParameters) {
        utmParameters = getUTMParameters();
      }

      eventsArray.push({
        event: eventName,
        data: eventData,
        timestamp: new Date().toISOString()
      });
      // Save eventsArray to sessionStorage:
      sessionStorage.setItem('eventsArray', JSON.stringify(eventsArray));

      console.log('Event tracked:', eventName, eventData);
    }

    // Send data to the server:
    function sendDataToServer() {
      if (eventsArray.length > 0) {
        const consolidatedData = {
          sessionId: sessionId,
          device: deviceInfo,
          ip: ip,
          utm: utmParameters,
          events: eventsArray
        };

        fetch('http://localhost:3000/analytic-data', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(consolidatedData)
        }).then(response => {
          if (response.ok) {
            eventsArray = []; // Clear the array after sending data
            sessionStorage.setItem('eventsArray', JSON.stringify(eventsArray));
            console.log('Data sent successfully');
          } else {
            console.error('Error in response:', response.statusText);
          }
        }).catch(error => {
          console.error('Error sending data:', error);
        });
      }
    }

    // Periodically send data to the server:
    //setInterval(sendDataToServer, 10000);

    // Reset the session timeout:
    function resetSessionTimeout() {
      clearTimeout(sessionTimeout);
      sessionTimeout = setTimeout(() => {
        console.log('Session expired');
        sendDataToServer(); // Send data before resetting session ID
        sessionId = generateSessionId();
        console.log('New session started:', sessionId);
      }, SESSION_TIMEOUT);
    }

    // Setup activity tracking for various events:
    function setupActivityTracking() {
      const events = ['click', 'keydown', 'mousemove'];
      events.forEach(event => {
        document.addEventListener(event, resetSessionTimeout);
      });
    }

    // Handle scroll events and track when scrollPercentLimit% of the page is scrolled:
    function handleScrollEvent() {
      if (!hasTriggered80PercentScroll) {
        const scrollPosition = window.scrollY + window.innerHeight;
        const pageHeight = document.documentElement.scrollHeight;
        const scrollPercent = (scrollPosition / pageHeight) * 100;
        if (scrollPercent >= scrollPercentLimit) {
          trackEvent('scroll', { page: window.location.pathname ,scrollPercent: scrollPercent });
          hasTriggered80PercentScroll = true;
          setupActivityTracking();
          resetSessionTimeout();
        }
      }
    }

    // Check if this is the first visit:
    function checkFirstVisit() {
      const isFirstVisit = !localStorage.getItem('hasVisited');
      if (isFirstVisit) {
        trackEvent('first_visit', {});
        localStorage.setItem('hasVisited', 'true');
      }
      return isFirstVisit;
    }

    // Handle click events and track click data:
    function handleClickEvent(event) {
      const element = event.target;
      const elementType = element.tagName.toLowerCase();
      const elementId = element.id || 'no-id';
      const elementClasses = element.className || 'no-classes';
      const clickX = event.clientX;
      const clickY = event.clientY;
      const page = window.location.pathname;

      trackEvent('click', { elementType, elementId, elementClasses, clickX, clickY, page });
    }

    // Add event listeners for scroll and click events:
    document.addEventListener('scroll', handleScrollEvent);
    document.addEventListener('click', handleClickEvent);

    // When the DOM is fully loaded, track the page view and setup activity tracking:
    document.addEventListener('DOMContentLoaded', async function() {
      const isFirstVisit = checkFirstVisit();
      utmParameters = getUTMParameters()
      await trackEvent('page_view', { page: window.location.pathname, firstVisit: isFirstVisit, utmParameters:utmParameters});
      setupActivityTracking();
      resetSessionTimeout();
    });

    // Track button clicks when the DOM is fully loaded:
    document.addEventListener('DOMContentLoaded', function() {
      document.querySelector('#myButton').addEventListener('click', function() {
        trackEvent('button_click', { page: window.location.pathname, buttonId: 'myButton' });
        setupActivityTracking();
        resetSessionTimeout();
      });
    });
    </script>
""", unsafe_allow_html=True)
