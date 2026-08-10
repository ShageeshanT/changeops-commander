document.addEventListener('DOMContentLoaded', () => {
  const btnSimulate = document.getElementById('btn-simulate');
  const incidentList = document.getElementById('incident-list');
  const timeline = document.getElementById('agent-timeline');
  const eventsContainer = document.getElementById('events-container');
  const proposalCard = document.getElementById('proposal-card');
  
  const btnApprove = document.getElementById('btn-approve');
  const btnReject = document.getElementById('btn-reject');

  let currentStep = 0;
  let simulationInterval;

  function renderEvent(ev) {
    const el = document.createElement('div');
    el.className = `event ${ev.kind}`;
    
    let html = `
      <div class="event-time">${ev.ts}</div>
      <div class="event-content">
        <div class="event-title">${ev.title}</div>
        <div class="event-detail">${ev.detail}</div>
    `;
    
    if (ev.code) {
      html += `<div class="event-code">${ev.code}</div>`;
    }
    
    html += `</div>`;
    el.innerHTML = html;
    eventsContainer.appendChild(el);
    eventsContainer.scrollTop = eventsContainer.scrollHeight;
  }

  function showProposal(proposal) {
    document.getElementById('proposal-summary').textContent = proposal.summary;
    document.getElementById('proposal-commands').textContent = proposal.commands;
    document.getElementById('proposal-risk').textContent = `RISK: ${proposal.risk}`;
    proposalCard.classList.remove('hidden');
  }

  function runSimulation() {
    btnSimulate.disabled = true;
    
    // Update UI state
    document.querySelector('.service:nth-child(2)').classList.replace('green', 'red');
    incidentList.innerHTML = `
      <li class="incident-item active">
        <div class="title">checkout-api error spike</div>
        <div class="meta">Severity: SEV-2 | Status: Investigating</div>
      </li>
    `;
    
    timeline.classList.remove('hidden');
    eventsContainer.innerHTML = '';
    proposalCard.classList.add('hidden');
    currentStep = 0;

    simulationInterval = setInterval(() => {
      if (currentStep < mockIncidentEvents.length) {
        const ev = mockIncidentEvents[currentStep];
        renderEvent(ev);
        
        if (ev.proposal) {
          showProposal(ev.proposal);
          clearInterval(simulationInterval);
        }
        currentStep++;
      }
    }, 1500);
  }

  function executeApproval() {
    proposalCard.classList.add('hidden');
    
    let execStep = 0;
    const execInterval = setInterval(() => {
      if (execStep < mockExecutionEvents.length) {
        renderEvent(mockExecutionEvents[execStep]);
        
        if (execStep === mockExecutionEvents.length - 1) {
          document.querySelector('.service:nth-child(2)').classList.replace('red', 'green');
          document.querySelector('.incident-item .meta').textContent = 'Severity: SEV-2 | Status: Resolved';
          document.querySelector('.incident-item').classList.remove('active');
          btnSimulate.disabled = false;
        }
        execStep++;
      } else {
        clearInterval(execInterval);
      }
    }, 1500);
  }

  btnSimulate.addEventListener('click', runSimulation);
  btnApprove.addEventListener('click', executeApproval);
  
  btnReject.addEventListener('click', () => {
    proposalCard.classList.add('hidden');
    renderEvent({
      ts: "14:04:00",
      kind: "observe",
      title: "Proposal Rejected",
      detail: "Human operator rejected the rollback. Agent returning to planning phase or escalating."
    });
    btnSimulate.disabled = false;
  });
});
