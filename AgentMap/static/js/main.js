// I Also hate javascript, but it is what it is
        // Get the modal
        let modal = document.getElementById("PDFModal");

        // Function to open the modal and set the iframe src
        function openModal(url) {
            // Log the url
            console.log("Opening modal with url: " + url)
            // set the iframe src to the url
            document.getElementById("pdfIframe").src = url;
            // display the modal
            modal.style.display = "block";
        }

        // Function to close the modal and clear the iframe src
        function closeModal() {
            // clear the iframe src and hide the modal
            document.getElementById("pdfIframe").src = "";
            modal.style.display = "none";
        }

        // Reset the scroll position to the top of the page
        function resetScroll() {
            // Get the info-box container
            let infoBoxContainer = document.getElementById('info-box')
            infoBoxContainer.scrollTop = 0; // Scroll to the top of the container
        }

        // Lerp between header colors
        function HeaderLerp(){
            // Get the days_until_expiration value from the newly loaded content
            let daysUntilExpiration = parseInt(document.querySelector('#days-until-expiration').textContent);
            console.log("Expiration Timer: :" + daysUntilExpiration) // Log this shit quay

            // Get the last Color of the health bar from the .LastHPColor class
            // if it isn't empty, else default should be green [7, 170, 8]
            let lastColor = document.querySelector('.LastHPColor').textContent;
            console.log("Last Color: " + lastColor)
            // Check if lastColor string is correctly formatted
            // Regex Magicka
            if (/[^0-9.,]/.test(lastColor)) {
                // If lastColor contains non-numeric characters (other than commas and periods), remove them
                lastColor = lastColor.replace(/[^0-9.,]/g, ''); // Regex Magicka
            }

            // If the last color is empty use the default green color I like, else format the lastColor
            lastColor = lastColor === '' ? [43, 177, 100] : lastColor.split(',').map(Number);

            //Get the last width of the health bar from the .LastHPWidth class
            let lastWidthText = document.querySelector('.LastHPWidth').textContent;

            // If lastColor is not empty, immediately set the background color of the health bar
            if (lastColor !== '') {
                document.querySelector('.health-bar').style.backgroundColor = 'rgb(' + lastColor.join(',') + ')';
                // console.log("last Color is not empty " + lastColor)
            }
            if (lastWidthText.trim() === '') {
                document.querySelector('.health-bar').style.width = '100%';
            }

            // Set the lastWidth from the lastWidthText and clamp it between 0 and 100
            let lastWidth = parseFloat(lastWidthText);
            lastWidth = Math.max(0, Math.min(lastWidth, 100));

            // timeout to delay the lerp to look clean
            setTimeout(function() {
                // console.log("Delay the lerp to look clean")
            }, 80);

            let colorString = ''
            if(daysUntilExpiration === 9999) {
                colorString = 'rgb(43, 177, 100)' // default to green if maxed out
            } else if (daysUntilExpiration > 31 && daysUntilExpiration !== 9999) {
                colorString = 'rgb(43, 177, 100)' // Default to black since no date
            } else if(!isNaN(daysUntilExpiration)) {
                // Clamp DaysUntilExpiration between 0 and 31
                daysUntilExpiration = Math.max(0, Math.min(daysUntilExpiration, 31))
                // Calculate lerp Percentage
                let lerpPercentage = ((daysUntilExpiration) % 4) /4; // Cap it off at a month
                let index = Math.floor((daysUntilExpiration) / 4); // Get the index of the color point

                // Define Colors
                let colorPoints = [
                    [255, 38, 38], // red
                    [255, 92, 48], // orange kinda red
                    [255, 142, 57], //orange
                    [255, 192, 62], // yellow kinda orange
                    [255, 246, 76], // yellow
                    [200, 228, 82], // Yellow kinda green
                    [178, 222, 85], // Green more yellowish
                    [94, 194, 94], // green kinda yellow
                    [43, 177, 100], // green
                ]
                let colorInterpolated = []; // Empty array to store the interpolated color

                colorInterpolated = colorPoints[index].map(function (channel, channelIndex) {
                    return channel + (colorPoints[index + 1][channelIndex] - channel) * lerpPercentage;
                });

                colorString = 'rgb(' + colorInterpolated.join(',') + ')'; // format from bits to string

                // Apply the color to the h1 if the lerpPercentage is 0
                if(lerpPercentage === 0 && index === 0) {
                    document.querySelector('h1').style.color = colorString;
                }
            } else {
                colorString = 'oklch(0% 0 0)' // Default to black
            }

            // Get the health bar element
            let healthBar = document.querySelector('.health-bar');

            // Calculate the health bar width
            let healthBarWidth = (daysUntilExpiration / 31) * 100;

            // Clamp the health bar width between 0 and 100
            healthBarWidth = Math.max(0, Math.min(healthBarWidth, 100));

            // Get the current color of the health bar
            let currentColor = colorString.slice(4, -1).split(',').map(Number);

            // The difference between the current color and the last color
            let colorDiff = [
                currentColor[0] - lastColor[0], // Red channel
                currentColor[1] - lastColor[1], // Green channel
                currentColor[2] - lastColor[2] // Blue channel
            ];

            function calculateColor(percentage) {
                return 'rgb(' + lastColor.map(function (channel, index) {
                    return Math.round(channel + colorDiff[index] * percentage);
                }).join(',') + ')';
            }

            // create a dynamic animation
            let animName = 'HealthBar-Width';
            let animDuration = 1;

            // Create the keyframes for the animation
            let keyframes = `@keyframes ${animName} {
                from { width: ${lastWidth}%; background-color: ${lastColor};}
                to { width: ${healthBarWidth}%; background-color: ${colorString};
            }`;

            // Use requestAnimationFrame to update the color of the health bar at each frame
            let start;
            function frame(time){
                if(!start) start = time; // set the start time
                let progress = Math.min((time - start) / 1000, 1); // Calculate the progress between frames
                healthBar.style.background = calculateColor(progress); // Calculate the color
                if(progress < 1) {
                    requestAnimationFrame(frame); // Continue the animation
                }
            }
            requestAnimationFrame(frame) // Start the animation

            // Create a style element
            let style = document.createElement('style');

            // Set the style element text to the keyframes
            style.textContent = keyframes; // Put it as the text content for the style element for whatever reason

            document.head.appendChild(style); // Append the style element to the head

            // Apply the animation to the health bar
            // delay the animation by 30ms to look smoother
            healthBar.style.animation = `${animName} ${animDuration}s 1  ease-in-out forwards`;

            // document the width amount to the .LastHPWidth class
            document.querySelector('.LastHPWidth').textContent = healthBarWidth.toString();

            // document the color to the .LastHPColor class
            document.querySelector('.LastHPColor').textContent = colorString;

            // Set Timeout to hide the health bar if daysUntilExpiration is 0
            setTimeout(function() {
                if (daysUntilExpiration === 0) {
                    healthBar.style.display = 'none'; // Hide the health bar
                } else {
                    healthBar.style.display = 'block'; // Show the health bar
                }
            }, 800);
        }

        // Function to darken a color
        // Uses some bitwise operations to darken the color by a percentage.
        // Gotta review this later cause i have zero clue how bit-shifting changes the color.
        function darkenColor(color, percent) {
            // Convert the hex color to an integer
            let num = parseInt(color.replace("#",""), 16),  // Convert the color from hex to an integer
            amt = Math.round(2.55 * percent), // Calculate the amount to darken
            R = (num >> 16) + amt, // Shift the bits to get the red value
            B = (num >> 8 & 0x00FF) + amt, // Shift the bits to get the blue value
            G = (num & 0x0000FF) + amt; // Get the green value
            // Return the new color
            return "#" + (0x1000000 + (R<255?R<1?0:R:255)*0x10000 + (B<255?B<1?0:B:255)*0x100 + (G<255?G<1?0:G:255)).toString(16).slice(1);
        }

        // We want to create a new darkenColor function that uses only the oklch color space
        // This function will take in a color in the oklch color space and darken it by a percentage
        function darkenOKLCH(color, percent) {
            // Split the color into the L, C, and H values
            let colorArray = color.split(' '); // Split the color into an array
            console.log("Color Array: " + colorArray) // Log the color array
            let L = parseFloat(colorArray[0].replace('oklch(', '')); // Get the L value and remove the oklch( prefix
            let C = parseFloat(colorArray[1]); // Get the C value
            let H = parseFloat(colorArray[2]); // Get the H value
            console.log("Original Color: " + L + '% ' + C + ' ' + H) // Log the original color

            // Calculate the new L value
            let newL = L - (L * (percent / 100)); // Calculate the new L value

            // Return the new color in the oklch color space
            console.log("Darkened Color: " + newL + '% ' + C + ' ' + H)
            return 'oklch(' + newL + '% ' + C + ' ' + H + ')';
        }

        // Function to get current time in a specific time zone
function getTimeInTimeZone(timeZone) {
    // Create a date object for the current time
    let date = new Date();

    // Convert the current time to the time in the specified time zone
    let utc = date.getTime() + (date.getTimezoneOffset() * 60000);
    let newDate = new Date(utc + (3600000 * timeZone));

    // Format the time in HH:MM format
    let time = newDate.toISOString().substr(11, 8);

    // Convert the 24-hour time to 12-hour time with AM/PM
    let hours = newDate.getUTCHours();
    let minutes = newDate.getUTCMinutes();
    let ampm = hours >= 12 ? 'PM' : 'AM';
    hours = hours % 12;
    hours = hours ? hours : 12; // the hour '0' should be '12'
    minutes = minutes < 10 ? '0'+minutes : minutes;
    let strTime = hours + ':' + minutes + ' ' + ampm;

    // Return the time in the specified time zone
    return strTime;
}

// Function to update time-zone texts
function updateTimeZones() {
    // Get the text elements for the time zones
    let easternTime = document.querySelector("#Eastern");
    let centralTime = document.querySelector("#Central");
    let mountainTime = document.querySelector("#Mountain");
    let pacificTime = document.querySelector("#Pacific");

    // Update the text content with the current time in the respective time zone
    easternTime.textContent = getTimeInTimeZone(-8);
    centralTime.textContent = getTimeInTimeZone(-9);
    mountainTime.textContent = getTimeInTimeZone(-10);
    pacificTime.textContent = getTimeInTimeZone(-11);
}

// Update the time zones every second
function updateStateColorsAndTimeZones() {
            // Grabs all elements with the class tag "preload" and removes that extra tag
            document.querySelectorAll('.preload').forEach(function(element) {
                element.classList.remove('preload'); // Remove the preload class
            });

            // Get all the path, circle, and text elements
            let elements = document.querySelectorAll('#states path, #states circle, #states text');

            // Loop through each path, circle, and text element
            elements.forEach(function(element) {
                let state = element.id;
                let color = licensedStates[state];
                // console.log("Element: " + element) // Log this
                // console.log("State: " + state) // Log this
                // console.log("Color: " + color) // Log this


                // Check if the state is in the list of licensed states
                if (color) {
                    // Log the licensed state and color
                    // console.log("Licensed State: " + state) // Log this shit Quay
                    console.log("Updated Color: " + color) // Log This shit Quay

                    // Apply the color to the element
                    element.style.fill = color;

                    // Add a mouseover and mouseout event listener
                    element.addEventListener('mouseover', function() {
                        // Log the mouseover event
                        console.log("Mouseover Licensed State: " + element.id + " - " + color);

                        // Darken the color by 20% on hover and apply styling
                        //element.style.fill = darkenColor(color, -16); // Darken the color
                        element.style.fill = darkenOKLCH(color, 25)
                        element.style.strokeWidth = '2px'; // Set the line width to 2px
                        element.style.strokeLinejoin = 'round'; // Set the Stroke line join to round
                        element.style.transition = 'fill 850ms'; // transition effect
                        // If the element has class "stateName", also change the style of the corresponding path
                        if (element.classList.contains('stateName')) {
                            // Log the mouseover event
                            console.log("Mouseover Licensed State Name: " + element.id + " - " + color);

                            // get the path or circle element with the same id
                            let path = document.querySelector('path[id="' + element.getAttribute('id') + '"]');
                            let circle = document.querySelector('circle[id="' + element.getAttribute('id') + '"]');

                            // If the path or circle exists, change its style
                            if (path || circle) {
                                // Get the target element
                                let target = path ? path : circle;
                                target.style.strokeWidth = '2px'; // Set the stroke width to 2px
                                target.style.strokeLinejoin = 'round'; // Set the stroke line join to round
                                //target.style.fill = darkenColor(color, -16); // Darken the color by 20%
                                target.style.fill = darkenOKLCH(color, 25)
                                target.style.transition = 'fill 850ms';  // Set the transition to 850ms
                            }

                            // shift the color of the text to off-white
                            element.style.fill = 'oklch(0% 0 0)';
                        }
                    });

                    // Add a mouseout event listener
                    element.addEventListener('mouseout', function() {
                        // Log the mouseout event
                        console.log("Mouseout Licensed State: " + element.id + " - " + color);

                        // Reset the color on mouseout and remove styling
                        element.style.fill = color; // Reset the color
                        element.style.strokeWidth = ''; // Set the stroke width to nothing
                        element.style.strokeLinejoin = ''; // Set the stroke line join to nothing
                        element.style.transition = 'fill 850ms'; // Set the transition to 850ms

                        // If the element has class "stateName", also reset the style of the corresponding path
                        if (element.classList.contains('stateName')) {
                            // Log the mouseout event
                            console.log("Mouseout Licensed State Name: " + element.id + " - " + color)

                            // get the path or circle element with the same id
                            let path = document.querySelector('path[id="' + element.getAttribute('id') + '"]');
                            let circle = document.querySelector('circle[id="' + element.getAttribute('id') + '"]');

                            // If the path or circle exists, reset its style
                            if (path || circle) {
                                let target = path ? path : circle;
                                target.style.strokeWidth = ''; // Set the stroke width to nothing
                                target.style.strokeLinejoin = ''; // Set the stroke line join to nothing
                                target.style.fill = color; // Set the fill to the original color
                                target.style.transition = 'fill 850ms'; // Set the transition to 850ms
                            }
                            // Keep the color of the text black when the mouse is no longer hovering over it
                            element.style.fill = 'oklch(0% 0 0)'; // Black as my soul
                        }
                    });
                }
                else {
                    // Log the non-licensed state
                    // console.log("Non-Licensed State: " + state) // Log that shite Quay

                    // If it's not, apply a default color and hover effect
                    if (!element.classList.contains('stateName')) {
                        // Apply the default color and styling
                        element.style.fill = "oklch(84.52% 0 0)";  // Default color
                        element.style.strokeWidth = "2px"; // Set the stroke width to 2px
                        element.style.strokeLinejoin = "round"; // Set the stroke line join to round
                        element.style.transition = 'fill 850ms'; // Set the transition to 850ms
                    }
                    element.addEventListener('mouseover', function() {
                        // Log the mouseover event
                        console.log("Mouseover unlicensed state: " + element.id + " - oklch(84.52% 0 0)");

                        // If the element has class "stateName", keep its color black on hover
                        if (element.classList.contains('stateName')) {
                            // Log the mouseover event
                            console.log("Mouseover Unlicensed State Name: " + element.id + " - oklch(84.52% 0 0)");

                            // get the path or circle element with the same id
                            let path = document.querySelector('path[id="' + element.getAttribute('id') + '"]');
                            let circle = document.querySelector('circle[id="' + element.getAttribute('id') + '"]');
                            // If the path or circle exists, change its style
                            if (path || circle) {
                                let target = path ? path : circle; // Ternary Operator to select path or circle
                                target.style.strokeWidth = '2px'; // Set the stroke width to 2px
                                target.style.strokeLinejoin = 'round'; // Set the stroke line join to round
                                target.style.fill = darkenColor("#CCCCCC", -16); // Darken the color by 20%
                                target.style.transition = 'fill 850ms'; // Set the transition to 850ms
                            }
                            element.style.fill = 'oklch(0% 0 0)'; // Black as my soul
                        }
                        else {
                            // Darken the default color by 20% on hover
                            element.style.fill = darkenColor("#CCCCCC", -16); // Darken the color by 20%
                            element.style.strokeWidth = '2px';  // Set the stroke width to 2px
                            element.style.strokeLinejoin = 'round';  // Set the stroke line join to round
                            element.style.transition = 'fill 850ms'; // Set the transition to 850ms
                        }
                    });
                    element.addEventListener('mouseout', function() {
                        // Reset the color on mouseout
                        element.style.fill = "oklch(84.52% 0 0)"; // Default color
                        element.style.strokeWidth = ''; // Set the stroke width to nothing
                        element.style.strokeLinejoin = ''; // Set the stroke line join to nothing
                        element.style.transition = 'fill 850ms'; // Set the transition to 850ms

                        // Log the mouseout event
                        console.log("Mouseout Unlicensed State:" + element.id + " - #CCCCCC"); // Log that shit quay

                        // If the element has class "stateName", keep its color black when the mouse is no longer hovering over it
                        if (element.classList.contains('stateName')) {
                            // Log the mouseout event
                            console.log("Mouseout Unlicensed State Name: " + element.id + " - #CCCCCC");

                            // get the path or circle element with the same id
                            let path = document.querySelector('path[id="' + element.getAttribute('id') + '"]');
                            let circle = document.querySelector('circle[id="' + element.getAttribute('id') + '"]');

                            // If the path or circle exists, reset its style
                            if (path || circle) {
                                let target = path ? path : circle;
                                target.style.strokeWidth = ''; // Set the targets stroke width to nothing
                                target.style.strokeLinejoin = ''; // Set the targets stroke line join to nothing
                                target.style.fill = "oklch(84.52% 0 0)"; // Set the targets fill to the default color
                                target.style.transition = 'fill 850ms'; // Set the targets transition to 850ms
                            }
                            element.style.fill = 'oklch(0% 0 0)';
                        }

                    });
                }
                // If the element has class "stateName", set its color to black
                if (element.classList.contains('stateName')) {
                    element.style.fill = 'oklch(0% 0 0)'; // Black as my soul
                }
                // Update the time zones
                // Call the function to update the time zones
                updateTimeZones();
                // Set an interval to update the time zones every second
                setInterval(updateTimeZones, 1000);
            });
}

// on window load, update the state colors
window.onload = updateStateColorsAndTimeZones;

// add an event listener for the htmx:afterSwap event
// Basically whenever we pull up the company information, Mainly used for the color coding for HouseHold Discounts
document.body.addEventListener('htmx:afterSwap', function(event) {

    // Reset the scroll position to the top of the container
    resetScroll();

    // Update the state colors and time zones
    console.log("updating state colors and time zones")
    updateStateColorsAndTimeZones();

    // Lerp the header color
    setTimeout(HeaderLerp, 80);

    console.log("htmx:afterSwap event:" + event.detail.elt.id + " loaded");
});

function logComputedClampValue(selector, property) {
    // Select the element you want to inspect
    const element = document.querySelector(selector);

    if (!element) {
        console.error(`Element with selector "${selector}" not found.`);
        return;
    }

    // Get the computed styles of the element
    const computedStyles = window.getComputedStyle(element);

    // Get the specific property value
    const value = computedStyles.getPropertyValue(property);
    console.log(`Computed value of ${property}:`, value);
}

// Call the function with the desired selector and property
logComputedClampValue('.horizontal-container', 'height');

// Optionally, call the function on window resize
window.addEventListener('resize', () => logComputedClampValue('.horizontal-container', 'height'));