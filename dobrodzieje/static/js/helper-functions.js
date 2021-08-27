  // Injects all necessary data to the join request modal
  function joinModalControl() {
    const acceptButton = document.querySelectorAll('.js-accept-request');
    const rejectButton = document.querySelectorAll('.js-reject-request');
    const modalTitle = document.querySelector('#requestModal .js-modal-title');
    const modalBody = document.querySelector('#requestModal .js-modal-body');
    const modalForm = document.querySelector('#requestModal form');
    const modalCreatorInput = document.querySelector('#requestModal .js-creator-input');
    const modalTeamIDInput = document.querySelector('#requestModal .js-team-id-input');

    function populateForm(target, action) {
      const joinRequestType = target.dataset.joinRequestType;
      const formURL = target.dataset.formUrl.trim();
      const senderID = target.dataset.senderId;
      const senderEmail = target.dataset.senderEmail;
      const teamID = target.dataset.teamId;

      if (action === 'accept') {
        modalTitle.textContent = 'Potwierdź użytkownika';

        if (joinRequestType === 'Join Announcement Request') {
          modalBody.textContent = `Gdy potwierdzisz, użytkownik ten zacznie pracować nad Twoją stroną. Aby się z nim skontaktować wyślij do niego maila na adres ${senderEmail}.`;
        }
        else {
          modalBody.textContent = 'Gdy potwierdzisz, użytkownik ten dołączy do Twojej drużyny. Aby się z nim skontaktować wyślij do niego maila';
          modalTeamIDInput.value = teamID;
        }
      }
      else {
        modalTitle.textContent = 'Odrzuć użytkownika';

        if (joinRequestType === 'Join Announcement Request') {
          modalBody.textContent = 'Potwierdzając odrzucisz użytkownika od pracy nad Twoją stroną. Będzie on mógł jednak zgłosić się ponownie.';
        }
        else {
          modalBody.textContent = 'Potwierdzając odrzucisz użytkownika od pracy w Twojej drużynie. Będzie on mógł jednak zgłosić się ponownie.';
        }
      }

      modalForm.action = formURL;
      modalCreatorInput.value = senderID;
    }

    acceptButton.forEach(btn => btn.addEventListener('click', (e) => {
      populateForm(target=e.target, 'accept');
    }));

    rejectButton.forEach(btn => btn.addEventListener('click', (e) => {
      populateForm(target=e.target, 'reject');
    }));
}