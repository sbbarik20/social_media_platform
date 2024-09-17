document.addEventListener('DOMContentLoaded', () => {
    const postButton = document.getElementById('post-btn');
    const postContent = document.getElementById('post-content');
    const postsContainer = document.getElementById('posts');
    
    postButton.addEventListener('click', () => {
        const content = postContent.value.trim();
        
        if (content) {
            const postElement = document.createElement('div');
            postElement.className = 'post';
            postElement.innerHTML = `<p>${content}</p>`;
            
            postsContainer.prepend(postElement);
            postContent.value = ''; // Clear the textarea
        }
    });
});


function active(){
    let postspace = document.getElementById("feed");
    let text = document.getElementById("textbtn");
    if (postspace.style.display=="none") {
        postspace.style.display="block";
        text.innerHTML="Create new post";
    }else{
        postspace.style.display="none";
        text.innerHTML="Click here to Create new post";
    }
}