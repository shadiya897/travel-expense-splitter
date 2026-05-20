const homepage = document.getElementById('homepage');
const createTripPage = document.getElementById('createTripPage');

const createTripBtn = document.getElementById('createTripBtn');
const viewTripBtn = document.getElementById('viewTripBtn');
const homeBtn = document.getElementById('homeBtn');

const memberCountInput = document.getElementById('memberCount');
const memberInputsDiv = document.getElementById('memberInputs');


// -----------------------------
// Navigation
// -----------------------------

createTripBtn.addEventListener('click', () => {

    homepage.classList.add('hidden');
    createTripPage.classList.remove('hidden');

});

homeBtn.addEventListener('click', () => {

    createTripPage.classList.add('hidden');
    homepage.classList.remove('hidden');

});


// -----------------------------
// Dynamic Member Inputs
// -----------------------------

memberCountInput.addEventListener('input', () => {

    memberInputsDiv.innerHTML = "";

    const count = parseInt(memberCountInput.value);

    if (count > 0) {

        for (let i = 0; i < count; i++) {

            const input = document.createElement('input');

            input.type = "text";

            input.placeholder = `Member ${i + 1} Name`;

            input.className =
                "w-full border p-3 rounded-lg mb-3";

            input.required = true;

            memberInputsDiv.appendChild(input);
        }
    }
});


// -----------------------------
// Create Trip
// -----------------------------

document.getElementById('createTripForm')
.addEventListener('submit', async (e) => {

    e.preventDefault();

    const tripName =
        document.getElementById('tripName').value;

    const memberInputs =
        document.querySelectorAll('#memberInputs input');

    const members = [];

    memberInputs.forEach(input => {
        members.push(input.value);
    });

    const response = await fetch('/api/create_trip', {

        method: 'POST',

        headers: {
            'Content-Type': 'application/json'
        },

        body: JSON.stringify({
            name: tripName,
            members: members
        })

    });

    const data = await response.json();

    if (data.ok) {

        alert("Trip Created Successfully!");

        location.reload();

    } else {

        alert("Error Creating Trip");

    }

});