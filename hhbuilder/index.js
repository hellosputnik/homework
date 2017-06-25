// Attach the event handlers upon window load.
window.onload = function() {
    // Get the add button and attach the addPerson function as the event
    // handler.
    var addButton = document.querySelector("button.add");
    addButton.addEventListener("click", addPerson);

    // Get the submit button and attach the serialize function as the event
    // handler.
    var submitButton = document.querySelector("button[type=submit]");
    submitButton.addEventListener("click", serialize);
}


// ==== Helper functions =======================================================

// Get the age entered into the input.
function getAge() {
    // Get the input.
    var ageInput = document.querySelector("input[name=age]");

    // Get the age as a number.
    var age = Number(ageInput.value);
    return age;
}


// Get the relationship chosen from the select.
function getRelationship() {
    // Get the select.
    var relationshipSelect = document.querySelector("select[name=rel]");

    // Get the relationship.
    var relationship = relationshipSelect.value;
    return relationship;
}


// Get the smoker status.
function isSmoker() {
    // Get the input.
    var smokerInput = document.querySelector("input[name=smoker]");

    // Get the status.
    return smokerInput.checked;
}


// =============================================================================


// ==== main functions =========================================================

// Add a person as a list item to the household represented by an ordered list.
function addPerson(event) {
    // Do not reload the page, which is the default behavior of a button that
    // has been clicked.
    event.preventDefault();

    // Get and validate the age entered into the age input.
    var age = getAge();
    if (age <= 0 || isNaN(age)) {
        alert("Please enter in a valid age.");
        return;
    }

    // Get and validate the relationship entered into the relationship select.
    var relationship = getRelationship();
    if (relationship === "") {
        alert("Please select a valid relationship.");
        return;
    }

    // Get the smoker status.
    var smoker = isSmoker() ? "smoker" : "nonsmoker";

    // Get the ordered list.
    var household = document.querySelector("ol.household");

    // Create a list item.
    var person = document.createElement("li");
    person.textContent = relationship + " " + age + " " + smoker + " ";

    // Create a button that could remove the person from the household. This
    // is necessary for the case where the person dishonors his family by not
    // landing a job with Ad Hoc.
    var button = document.createElement("button");
    button.type = "button";
    button.textContent = "X";

    // Set the event handler for the button click.
    button.addEventListener("click", function() { this.parentNode.remove(); });

    // Add the button to the list item.
    person.appendChild(button);

    // Finally, add the person to the household (i.e., add the li to the ol).
    household.appendChild(person);
}


function serialize(event) {
    // Do not reload the page, which is the default behavior of a button that
    // has been clicked.
    event.preventDefault();

    // Get the household.
    var household = document.querySelector("ol.household");

    // Loop through the household and add each member as an object to the JSON
    // list of household members.
    var members = { household: [] };
    for (var i = 0; i < household.children.length; ++i) {
        // Get the household member's information.
        person = household.children[i].textContent.split(" ");

        // Construct the object. This can be be more cleanly written by passing
        // the data to a "constructor".
        member = {};
        member.relationship = person[0];
        member.age          = Number(person[1]);
        member.smoker       = person[2] === "smoker";

        // Add the object to the list.
        members.household.push(member);
    }

    // Get the debug element.
    var debug = document.querySelector("pre.debug");

    // Put the serialize JSON in the provided debug pre element and display the
    // element.
    debug.style.display = "block";
    debug.textContent = JSON.stringify(members, null, 2);
}

// =============================================================================

