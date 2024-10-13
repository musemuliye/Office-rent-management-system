function sidebar_data() {
  fetch("{% url 'idebar-data' %}")
    .then((response) => response.json())
    .then((data) => {
      document.getElementById("blocks-count").textContent = data;
    })
    .catch((error) => console.error("Error fetching counts:", error));
}

// Fetch data every 30 seconds
setInterval(fetchCounts, 30000);

// Initial fetch
fetchCounts();
