document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchTerm');
    const searchBtn = document.getElementById('searchBtn');
    const resultContainer = document.getElementById('result');
    const explanationEl = document.getElementById('explanation');
    const trendSection = document.getElementById('trendSection');
    const trendEl = document.getElementById('trend');
    const newsSection = document.getElementById('newsSection');
    const newsEl = document.getElementById('news');
    const popularKeywordsContainer = document.getElementById('popularKeywords');

    // 초기 인기 키워드 로딩
    loadPopularKeywords();

    // 인기 키워드 로딩 함수
    async function loadPopularKeywords() {
        try {
            const response = await fetch("http://127.0.0.1:5000/keywords");
            const data = await response.json();
            
            if (data.keywords && data.keywords.length > 0) {
                popularKeywordsContainer.innerHTML = data.keywords
                    .map(keyword => `<button class="keyword-btn">${keyword}</button>`)
                    .join('');
                
                // 키워드 버튼에 이벤트 리스너 추가
                document.querySelectorAll('.keyword-btn').forEach(btn => {
                    btn.addEventListener('click', function() {
                        searchInput.value = this.textContent;
                        performSearch();
                    });
                });
            }
        } catch (error) {
            console.error("키워드 로딩 중 에러 발생:", error);
            popularKeywordsContainer.innerHTML = "키워드를 불러오는 중 오류가 발생했습니다.";
        }
    }

    // 검색 버튼 클릭 이벤트
    searchBtn.addEventListener('click', () => {
        performSearch();
    });

    // Enter 키 이벤트
    searchInput.addEventListener('keydown', function(event) {
        if (event.key === "Enter") {
            performSearch();
        }
    });

    // 검색 수행 함수
    async function performSearch() {
        const term = searchInput.value.trim();
        
        if (!term) {
            alert("금융 용어를 입력하세요!");
            return;
        }

        // 로딩 상태 표시
        showLoadingState();

        try {
            const response = await fetch("http://127.0.0.1:5000/explain?term=" + encodeURIComponent(term));
            const data = await response.json();
            
            // 결과 표시
            updateUI(data);
            resultContainer.style.display = "block";

        } catch (error) {
            console.error("검색 중 에러 발생:", error);
            showErrorState();
        }
    }

    // 로딩 상태 표시 함수
    function showLoadingState() {
        resultContainer.style.display = "block";
        explanationEl.innerHTML = "🔄 정보를 불러오는 중...";
        document.querySelector('.section').classList.add('visible');
        trendSection.classList.remove('visible');
        newsSection.classList.remove('visible');
        trendEl.innerHTML = "";
        newsEl.innerHTML = "";
    }

    // 에러 상태 표시 함수
    function showErrorState() {
        resultContainer.style.display = "block";
        explanationEl.innerHTML = "❌ 정보를 가져오는 중 오류가 발생했습니다.";
        document.querySelector('.section').classList.add('visible');
        trendSection.classList.remove('visible');
        newsSection.classList.remove('visible');
    }

    // UI 업데이트 함수
    function updateUI(data) {
        // 설명 업데이트
        if (data.explanation) {
            explanationEl.innerHTML = data.explanation;
            document.querySelector('.section').classList.add('visible');
        }
        
        // 트렌드 업데이트
        if (data.trend && data.trend.trim()) {
            trendEl.innerHTML = data.trend;
            trendSection.classList.add('visible');
        }

        // 뉴스 업데이트
        if (data.news && data.news.length > 0) {
            newsEl.innerHTML = `<ul>${data.news
                .map(news => `<li class="news-item">
                    <a href="${news.link}" target="_blank">${news.title}</a>
                </li>`)
                .join('')}</ul>`;
            newsSection.classList.add('visible');
        }
    }
});