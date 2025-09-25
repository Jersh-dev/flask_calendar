        //calendar.js
        //This is the JavaScript used in the Flask Calendar Project
        
        // Get today's date
        const today = new Date();

        // Element for displaying current month and year
        const monthYear = document.getElementById("month-year");


        // Array of month names (to convert from number → text)
        const months = [
            "January","February","March","April","May","June",
            "July","August","September","October","November","December"
        ];

        // Track current month and year (start with today)
        let currentMonth = today.getMonth();
        let currentYear = today.getFullYear();

         /**
         * Render the calendar grid
         * @param {number} month - The month index (0=Jan, 11=Dec)
         * @param {number} year - Full year number
         * @param {Array} events - List of event objects from Flask
         */

        // Function to render the calendar
        function renderCalendar(month, year, events = []) {
            
            // Update header to show month year
            const monthYear = document.getElementById("month-year");
            monthYear.textContent = months[month] + " " + year;

            // Get which day of week the month starts on (0=Sunday, 6=Saturday)
            const firstDay = new Date(year, month).getDay();

            // Get total number of days in the month
            // (Day 0 of next month gives last day of current month)
            const daysInMonth = new Date(year, month + 1, 0).getDate();
            
            // Reference to calendar body <tbody>
            const body = document.getElementById("calendar-body");
            body.innerHTML = ""; // Clear out any existing rows before re-rendering


            let date = 1; // Start counting from day 1

            // Max 6 weeks in a month
            for (let i = 0; i < 6; i++) { 
                let row = document.createElement("tr");

                // Create 7 cells (Sun-Sat)
                for (let j = 0; j < 7; j++) { // 7 days in a week
                    let cell = document.createElement("td");

                    // Fill empty cells before first day of month
                    if (i === 0 && j < firstDay) {
                        cell.textContent = "";
                    }
                    // Stop filling when days exceed month length
                    else if (date > daysInMonth) {
                        break;
                    }
                    else {
                        // Create date string YYYY-MM-DD for this cell
                        let dateStr = `${year}-${String(month+1).padStart(2,'0')}-${String(date).padStart(2,'0')}`;

                        // Add date number at the top of the cell
                        cell.innerHTML = `<strong>${date}</strong> <br>`;

                        // Highlight today
                        if (
                            date === today.getDate() &&
                            year === today.getFullYear() &&
                            month === today.getMonth()
                        ) {
                            cell.classList.add("today");
                        }
                        // Insert events for this day
                        events.forEach(ev => {
                          // Extract date part from event.start (YYYY-MM-DDTHH:MM)
                          let eventDate = ev.start.split("T")[0];
                          if (eventDate === dateStr) {
                            //Create Event Label
                            let div = document.createElement("div");
                            div.className = "event";
                            div.textContent = ev.title; 
                            
                         
                            // Add Edit-on-click
                            div.addEventListener("click", function(e) {
                              e.stopPropagation(); //prevent triggering the <td> redirect
                              let newTitle = prompt("Edit Event Title:", div.textContent);
                              if (newTitle) {
                                div.textContent = newTitle;
                              
                              }
                            });
                            cell.appendChild(div);  // Add event to cell
                          }  
                        });

                        // Add data attribute to store full date
                        //cell.setAttribute("data-date", `${year}-${month+1}-${date}`);

                        // Add click handler to schedule event
                        cell.addEventListener("click", () => {
                            // For now → redirect to Flask form
                            window.location.href = `/add_event?date=${dateStr}`;
                        });

                        // Move to next date
                        date++;
                    }
                    // Add cell to row
                    row.appendChild(cell);
                }
                // Add row to table body
                body.appendChild(row);
            }
        }

        function prevMonth() {
          currentMonth--; //step back one month
          if (currentMonth < 0) {
            currentMonth = 11; // wrap back to december
            currentYear--; //decrease year
          }
          loadAndRenderCalendar();
        }
        function nextMonth() {
          currentMonth++; //step forward one month
          if (currentMonth > 11) {
            currentMonth = 0; //wrap forward to january
            currentYear++; //increase year
          }
          loadAndRenderCalendar();
        }

        document.addEventListener("DOMContentLoaded", function() {
            const prevBtn = document.getElementById("prev-month");
            const nextBtn = document.getElementById("next-month");
            prevBtn.addEventListener("click", prevMonth);
            nextBtn.addEventListener("click", nextMonth);
        });

        // Delegate event editing (when an event div is clicked)
        document.addEventListener("click", function(e){
          if (e.target.classList.contains("event")) {
            let newTitle = prompt("Edit Event Title:", e.target.textContent);
            if (newTitle) {
                e.target.textContent = newTitle; //Update Text 
            }
          }  
        });


        //Helper to fetch events and render
        function loadAndRenderCalendar() {
          fetch("/events")
          .then(response => response.json())
          .then(data => {
            renderCalendar(currentMonth, currentYear, data);
          });
        }

      loadAndRenderCalendar();