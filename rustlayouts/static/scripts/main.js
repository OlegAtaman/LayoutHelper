var audio = new Audio(staticUrl + 'sounds/upgradesound.m4a');
audio.play();

document.addEventListener('DOMContentLoaded', function() {
    var addButton = document.getElementById("add_large_box");
    addButton.addEventListener('click', function() {
        var newButton = document.createElement('button');
        newButton.className = 'remove_large_box'; // Use a class instead of ID
        newButton.textContent = 'Large box';
        newButton.addEventListener('click', function() {
            this.remove(); // `this` refers to the button that was clicked
        });
        document.getElementById("selected_items_list").appendChild(newButton);
    });
    document.getElementById("place_items").addEventListener('click', function() {
        elements = document.getElementsByClassName('large_box_c');
        while(elements.length > 0) {
            elements[0].parentNode.removeChild(elements[0]);
        }
        // for (let step = 0; step < document.getElementById("selected_items_list").childElementCount; step++) {
        //     var large_box = document.createElement('img');
        //     large_box.setAttribute("class", "large_box_c");
        //     large_box.setAttribute("src", staticUrl + "textures/large_box.png");
        //     large_box.setAttribute("id", "large_box"+step);
        //     document.getElementById('canvas').appendChild(large_box);
        //     console.log('placed');
        // };
    });
    document.getElementById("place_items").addEventListener('click', function() {
        let selected_items = [];
        let item_buttons = document.getElementById("selected_items_list").children;
    
        for (let i = 0; i < item_buttons.length; i++) {
            selected_items.push(item_buttons[i].textContent.toLowerCase().replace(" ", "_"));
        }
    
        fetch('/calculate_placement?items[]=' + selected_items.join('&items[]='), {
            method: 'GET'
        })
        .then(response => response.json())
        .then(data => {
            // Clear previously placed items
            document.querySelectorAll('.large_box_c').forEach(item => item.remove());
    
            // Place new items based on the server response
            data.placed_items.forEach(function(item, index) {
                var img = document.createElement('img');
                img.setAttribute("class", "large_box_c");
                img.setAttribute("src", staticUrl + "textures/" + item.item + ".png");
                img.style.position = 'absolute';
                img.style.left = item.x + 'px';
                img.style.top = item.y + 'px';
                img.style.width = item.width + 'px';
                img.style.height = item.height + 'px';
                document.getElementById('canvas').appendChild(img);
            });
        })
        .catch(error => console.log('Error:', error));
    });
});


