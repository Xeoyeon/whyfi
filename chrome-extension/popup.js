document.getElementById("searchBtn").addEventListener("click", async () => {
    performSearch();
});

document.getElementById("searchTerm").addEventListener("keydown", function(event) {
    if (event.key === "Enter") {
        performSearch();  
    }
});

document.getElementById("clearBtn").addEventListener("click", function() {
    document.getElementById("searchTerm").value = "";
    this.style.display = "none";
});

async function performSearch() {
    const term = document.getElementById("searchTerm").value.trim();
    const resultDiv = document.getElementById("result");
    const newsDiv = document.getElementById("news");
    const clearBtn = document.getElementById("clearBtn");

    if (!term) {
        alert("금융 용어를 입력하세요!");
        return;
    }

    resultDiv.innerHTML = "🔄 정보를 불러오는 중...";
    newsDiv.innerHTML = "";

    try {
        const response = await fetch("http://127.0.0.1:5000/explain?term=" + encodeURIComponent(term));
        const data = await response.json();

        resultDiv.innerHTML = `<strong>설명:</strong><p>${data.explanation}</p>`;

        if (data.news.length > 0) {
            let newsHtml = "<ul>";
            data.news.forEach(news => {
                newsHtml += `<li><a href="${news.link}" target="_blank">${news.title}</a></li>`;
            });
            newsHtml += "</ul>";
            newsDiv.innerHTML = newsHtml;
        } else {
            newsDiv.innerHTML = "관련 뉴스가 없습니다.";
        }
        newsDiv.style.display = "block";
        
        // 검색 결과가 있으면 지우기 버튼 표시
        clearBtn.style.display = "inline-block"; 

    } catch (error) {
        console.error("에러 발생:", error);
        resultDiv.innerHTML = "❌ 정보를 가져오는 중 오류 발생";
    }
}




