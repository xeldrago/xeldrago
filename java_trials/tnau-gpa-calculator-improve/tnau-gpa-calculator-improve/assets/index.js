/*==================== DARK LIGHT THEME ====================*/ 
const themeButton = document.getElementById('theme-button')
const darkTheme = 'dark-theme'
const iconTheme = 'uil-sun'

// Previously selected topic (if user selected)
const selectedTheme = localStorage.getItem('selected-theme')
const selectedIcon = localStorage.getItem('selected-icon')

// We obtain the current theme that the interface has by validating the dark-theme class
const getCurrentTheme = () => document.body.classList.contains(darkTheme) ? 'dark' : 'light'
const getCurrentIcon = () => themeButton.classList.contains(iconTheme) ? 'uil-moon' : 'uil-sun'

// We validate if the user previously chose a topic
if (selectedTheme) {
  // If the validation is fulfilled, we ask what the issue was to know if we activated or deactivated the dark
  document.body.classList[selectedTheme === 'dark' ? 'add' : 'remove'](darkTheme)
  themeButton.classList[selectedIcon === 'uil-moon' ? 'add' : 'remove'](iconTheme)
}
function toggleMode(){
    // Add or remove the dark / icon theme
    document.body.classList.toggle(darkTheme)
    themeButton.classList.toggle(iconTheme)
    // We save the theme and the current icon that the user chose
    localStorage.setItem('selected-theme', getCurrentTheme())
    localStorage.setItem('selected-icon', getCurrentIcon())
}
// Activate / deactivate the theme manually with the button
themeButton.addEventListener('click', toggleMode)

// select main head

const courseSection = document.getElementById('r1');
const streamSection = document.getElementById('r2');
const semasterSection = document.getElementById('r3');
const gpaSection = document.getElementById('r4');
const downloadRes = document.getElementById('r5');
const footer = document.getElementById('r6');

const instruction = document.getElementById('Instructions')
const instructionBlock = document.getElementById('instructionBlock')



instruction.addEventListener('click', ()=>{
    instructionBlock.classList.toggle("instruction-show")
})


const courses = Object.keys(Information)
selectedCourse = NaN;

selectedCourseStreams = NaN;
selectedStream = NaN;

selectedStreamSemesters = NaN;
selectedSemaster = NaN;


totalCreditPoints = 0;
totalCreditHours = 0;

createCourseSection();

function clearSection(section){
  if(section!=null){
    while(section.firstChild){
        section.removeChild(section.lastChild);
    }
  }
  
}
// creating courses form available courses
function createCourseSection(){
    clearSection(courseSection);
    clearSection(streamSection);
    clearSection(semasterSection);
    clearSection(gpaSection);

    courses.forEach(course => {
        courseSection.appendChild(createCourseElement(course));
    });    
}

function createCourseElement(course){
    let element = document.createElement('div')
    element.textContent = course
    element.classList.add('course__element');
    element.addEventListener('click', ()=>{
        const streamElements = document.querySelectorAll('.course__element');
        streamElements.forEach(c=>{
            c.classList.remove('selected')
        });
        element.classList.add('selected')
        selectedCourse = element.innerHTML;
        selectedCourseStreams = Object.keys(Information[selectedCourse]);
        console.log(selectedCourseStreams)
        instructionBlock.classList.remove("instruction-show")
        createStreamSection()
    })
    return element
}

// create stream section from selected course 
function createStreamSection(){
    clearSection(streamSection);
    clearSection(semasterSection);
    clearSection(gpaSection);
    footer.classList.add('footer-show');
    selectedCourseStreams.forEach(stream => {
        streamSection.appendChild(createStreamElement(stream));
    });    
}

function createStreamElement(stream){
    let element = document.createElement('div')
    element.textContent = stream
    element.classList.add('stream__element');
    element.addEventListener('click', ()=>{
        const streamElements = document.querySelectorAll('.stream__element');
        streamElements.forEach(c=>{
            c.classList.remove('selected')
        });
        element.classList.add('selected')
        selectedStream = element.innerHTML;
        selectedStreamSemesters = Object.keys(Information[selectedCourse][selectedStream]);
        createsemasterSection();
    })
    return element
}

// semester section
function createsemasterSection(){
    clearSection(semasterSection);
    clearSection(gpaSection);
    console.log(selectedStreamSemesters);
    selectedStreamSemesters = selectedStreamSemesters.slice(1, );

    selectedStreamSemesters.forEach(semaster => {
        semasterSection.appendChild(createSemasterElement(semaster));
    });    
}

function createSemasterElement(semaster){
    let element = document.createElement('div')
    element.textContent = semaster
    element.classList.add('semaster__element');
    element.addEventListener('click', ()=>{
        const streamElements = document.querySelectorAll('.semaster__element');
        streamElements.forEach(c=>{
            c.classList.remove('selected')
        });
        element.classList.add('selected')
        selectedSemaster = element.innerHTML;
        console.log(selectedSemaster);

        // selectedStreamSemesters = Object.keys(Information[selectedCourse][selectedStream]);
        createGpaSection();
    })
    return element
}

//subject section
function infoSection(){
    let div = document.createElement('div');
    
    courseInfo = Information[selectedCourse][selectedStream]['course'];
console.log(courseInfo);
    let h1 = document.createElement('h1')
    h1.textContent = courseInfo
    h1.classList.add('section__title')
    div.appendChild(h1)

    let span = document.createElement('h3')
    span.textContent = selectedSemaster;
    span.classList.add('section__subtitle');
    div.appendChild(span);

    return div

}

function createSubjectElement(subject){
    let div = document.createElement('div');
    
    let subName = document.createElement('h2');
    subName.textContent = subject['Course No.'] + " " + subject['Course Title'];
    subName.classList.add('subject__name');
  
    var input = document.createElement("INPUT");
    input.id = subject['Course No.']
    input.setAttribute("type", "number")
    input.setAttribute("min", 40)
    input.setAttribute("max", 100);
    input.classList.add('subject__score');

    div.appendChild(subName);
    div.appendChild(input);
    div.classList.add('items');
    return div
}

function createSubjectSection(){
    let div = document.createElement('div');
    let div11 = document.createElement('div');
    
    let sub = document.createElement('h2');
    sub.textContent = "Subjects";
    div11.appendChild(sub);

    let score = document.createElement('h2');
    score.textContent = "Score";
    div11.appendChild(score);

    div11.classList.add('items');
    div.appendChild(div11);
    // console.log(selectedSemaster);

    subjects = [...Information[selectedCourse][selectedStream][selectedSemaster]];
    console.log(subjects)
    let p = document.createElement('p');
    p.textContent = "data yet to be collected";
    p.classList.add('flag')

    if (subjects.length === 0){
        div.append(p)
    }
    subjects.forEach(subject => {
        div.appendChild(createSubjectElement(subject));
    }); 
    // }
   
    return div;
}


function resSection(){
    let div = document.createElement('div');
    
    let gpaCalBtn = document.createElement('h1');
    gpaCalBtn.textContent = "Cal GPA"
    gpaCalBtn.classList.add('button');

    gpaCalBtn.addEventListener("click", calculateGpa);
    div.appendChild(gpaCalBtn);
    
    let subDiv = document.createElement('div');
    subDiv.classList.add("section")
    let tcp = document.createElement('h1');
    tcp.id = "tcp";
    tcp.classList.add("result__element")
    subDiv.appendChild(tcp)

    let tch = document.createElement('h1');
    tch.id = "tch";
    tch.classList.add("result__element")
    subDiv.appendChild(tch)

    let gpa = document.createElement('h1')
    gpa.id = "gpa"
    gpa.classList.add("result__element")
    subDiv.appendChild(gpa)
    // subDiv.classList.add('items');

    let printOut = document.createElement('h1')
    printOut.id = "printout"
    subDiv.appendChild(printOut)

    div.appendChild(subDiv);
    div.classList.add("grid")

    return div
    
    
}
function createGpaSection(){
    clearSection(gpaSection);
    gpaSection.appendChild(infoSection());
    gpaSection.appendChild(createSubjectSection());
    gpaSection.appendChild(resSection());
} 

function parseExp(str){
    str = str.replace('#', '')
    str = str.replace('*', '')
    str = str.replace('^', '')
    return str
}
function createResultTableElement(element){
  let ele = document.createElement('h2');
  ele.textContent = element;
  return ele
}

function generateResult(){
    // section = document.createElement('section')
    // section.id = "result"
    // section.classList.add("section")
    clearSection(downloadRes);
    downloadRes.appendChild(infoSection());
    
    let table = document.createElement('div');
    table.classList.add('table')
    heads = ["Subjects", 'Score', 'Credit Hours', "Grade Points", "Credit Points"]
    heads.forEach(head => {
      table.appendChild(createResultTableElement(head))
    });
    
    subjects.forEach(sub =>{
      element = sub['Course No.'] + " " + sub['Course Title'];
      table.appendChild(createResultTableElement(element))
      if('score' in sub){
        table.appendChild(createResultTableElement(sub['score']))
        table.appendChild(createResultTableElement(sub['Credit Hours']))
        table.appendChild(createResultTableElement(sub['gp'].toFixed(3)))
        table.appendChild(createResultTableElement(sub['cp'].toFixed(3)))
      }
      else{
        table.appendChild(createResultTableElement(0))
        table.appendChild(createResultTableElement(sub['Credit Hours']))
        table.appendChild(createResultTableElement(0))
        table.appendChild(createResultTableElement(0))
      }
    })
    downloadRes.appendChild(table)

    let subDiv = document.createElement('div');
    subDiv.classList.add("section")
    let tcp = document.createElement('h1');
    tcp.textContent =  "total Credit Points : " + totalCreditPoints.toFixed(3);
    tcp.classList.add("result__element")
    subDiv.appendChild(tcp)

    let tch = document.createElement('h1');
    tch.textContent = "total Credit Hours : " + totalCreditHours.toFixed(3);
    tch.classList.add("result__element")
    subDiv.appendChild(tch);

    gpaAns = totalCreditPoints/totalCreditHours;

    let gpa = document.createElement('h1')
    gpa.textContent = "GPA : " + gpaAns.toFixed(3);
    gpa.classList.add("result__element");

    subDiv.appendChild(gpa);
    downloadRes.appendChild(subDiv)

    // section.classList.add("hide")

    // let subName = document.createElement('h2');
    // subName.textContent = subject['Course No.'] + " " + subject['Course Title'];
    // subName.classList.add('subject__name');


}

// gpa calculate
function calculateGpa() {
    totalCreditPoints = 0;
    totalCreditHours = 0;
    // alert("clicked");
    console.log(subjects);
    subjects.forEach(element => {
        // get Actual grade and add to the dictionary

        id = element["Course No."]
        const sub = document.getElementById(id);
        // console.log(sub);
        givenValue = sub.value;
        console.log(givenValue);
        if (givenValue){

            gradePoints = parseFloat(givenValue);
            console.log(gradePoints);
            element['score'] = gradePoints

            gradePoints = (gradePoints/100) * 10;
            creditHours = eval(parseExp(element['Credit Hours']));
    
            element['gp'] = gradePoints;
            element['cp'] = gradePoints * creditHours;
    
            // console.log(element);
            
            // cal total
            totalCreditPoints +=  element['cp'];
    
            totalCreditHours+=creditHours 
        }            
    });
    gpa = totalCreditPoints/totalCreditHours;
    // gpa.parseFloat(2);
    const tcpRes = document.getElementById('tcp');
    tcpRes.innerHTML = "total Credit Points : " + totalCreditPoints.toFixed(3);
    
    const tchRes = document.getElementById('tch');
    tchRes.innerHTML = "total Credit Hours : " + totalCreditHours.toFixed(3);

    const gpaRes = document.getElementById('gpa');
    gpaRes.innerHTML = "GPA : " + gpa.toFixed(3);
    console.log(subjects);
    
    generateResult();

    // printing result to user
    const printOut = document.getElementById('printout');
    console.log(printOut.removeEventListener("click", downloadEvents));
    printOut.classList.add('button');
    printOut.innerHTML = "Download result";
    printOut.addEventListener("click",downloadEvents);

    // console.log(subjects);
  }
  function downloadEvents(){
    generatePDF("r5")
  }
  function generatePDF(id) {
    let changed = 0;  
    // toggleMode();

    if(getCurrentTheme().valueOf() == 'dark'.valueOf()){
      console.log(getCurrentTheme());
      toggleMode();
      changed=1;
    }
    let opt = {
        margin : 1,
        filename: selectedSemaster + " result",
        enableLinks: true,
        image: { type: 'png', quality: 1 },
        html2canvas: {
            scale: 2,
            useCORS: true,
            letterRendering: true,
        },
        jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' },
    }
    html2pdf().set(opt).from(document.getElementById(id)).save();

    if(changed==1){
      // toggleMode(); 
    }
}