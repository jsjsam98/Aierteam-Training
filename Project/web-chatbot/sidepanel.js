async function getCurrentTabInfo() {
	const [tab] = await chrome.tabs.query({
		active: true,
		currentWindow: true,
	});

	try {
		const response = await chrome.tabs.sendMessage(tab.id, {
			action: "getInfo",
		});
		return {
			url: response.url,
			links: response.links,
			titles: response.titles,
			innerText: response.innerText,
		};
	} catch (error) {
		console.error("Error getting HTML:", error);
		return null;
	}
}

async function getSummaryFromOpenAI(text) {
	try {
		const response = await fetch(
			"https://api.openai.com/v1/chat/completions",
			{
				method: "POST",
				headers: {
					"Content-Type": "application/json",
					Authorization: "Bearer " + "your-api-key-here",
				},
				body: JSON.stringify({
					model: "gpt-4o-mini",
					messages: [
						{
							role: "user",
							content: `Please summarize this webpage content in 100 words: ${text}`,
						},
					],
				}),
			}
		);

		const data = await response.json();
		return data.choices[0].message.content;
	} catch (error) {
		throw new Error(`Failed to get summary: ${error.message}`);
	}
}

function updateLinks(links) {
	const linksContainer = document.getElementById("links");
	linksContainer.innerHTML = ""; // Clear existing links

	links.forEach((link) => {
		const linkElement = document.createElement("a");
		linkElement.href = link;
		linkElement.textContent = link;
		linkElement.target = "_blank";
		linksContainer.appendChild(linkElement);
	});
}

async function updateContent() {
	const textarea = document.getElementById("summary");
	textarea.value = "Loading...";

	try {
		const pageInfo = await getCurrentTabInfo();
		if (!pageInfo) {
			throw new Error("Could not get page information");
		}

		// Update links section
		updateLinks(pageInfo.links);

		let content = "";

		// Get and append summary
		try {
			const summary = await getSummaryFromOpenAI(pageInfo.innerText);
			content += "Page Summary:\n" + summary;
		} catch (error) {
			content += "Error generating summary: " + error.message;
		}

		textarea.value = content;
	} catch (error) {
		textarea.value =
			"Error: Could not load content. Please refresh and try again.";
		console.error("Error:", error);
	}
}

document.addEventListener("DOMContentLoaded", () => {
	// only refresh when button is clicked
	// updateContent();

	const refreshButton = document.getElementById("refreshButton");
	refreshButton.addEventListener("click", updateContent);
});

document
	.querySelector("#links-section h2")
	.addEventListener("click", function () {
		document.getElementById("links").classList.toggle("show");
	});
