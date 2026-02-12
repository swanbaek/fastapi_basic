document.addEventListener("DOMContentLoaded", function() {
    loadMemoList();
    // 메모 목록 가져오기

    const memoForm = document.getElementById("memo-form");
    const authorInput = document.getElementById("author");
    const contentInput = document.getElementById("content");
    //const memoInput = document.getElementById("memo-input");
    //const memoList = document.getElementById("memo-list");  

    
    //글쓰기
    memoForm.addEventListener("submit", async function(event) {
        event.preventDefault(); // 폼 제출 기본 동작 방지   
        const author = authorInput.value.trim();
        const content = contentInput.value.trim();
        if (!(author && content)) {
            alert("작성자와 메모 내용을 모두 입력해주세요.");
            return;
        }
        //alert(author + ':' + content);
        
        const result= await fetch('/memo',{
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'  
            },
            body: JSON.stringify({ author, content })  
        })
        const data = await result.json();
        console.log('서버 응답:', data);
        //alert(data.message);
        authorInput.value = '';
        contentInput.value = '';
        // 메모 등록 후 목록 갱신
        loadMemoList();
    });

    // 삭제 버튼 ajax
    document.getElementById('memo-list-body').addEventListener('click', async function(e) {
        if (e.target.classList.contains('delete-btn')) {
            const id = e.target.dataset.id;
            if (confirm('삭제하시겠습니까?')) {
                await fetch(`/memo/${id}`, { method: 'DELETE' });
                loadMemoList();
            }
        }
    });
})

// 메모 목록 ajax로 갱신 (page 파라미터 지원)
async function loadMemoList(page=1) {
    const res = await fetch(`/memo/list?page=${page}`);
    const html = await res.text();
    document.getElementById('memo-list-body').innerHTML = html;
    // 페이징 버튼 이벤트 바인딩
    document.querySelectorAll('.page-btn').forEach(btn => {
        btn.onclick = function() {
            loadMemoList(this.dataset.page);
        };
    });
}