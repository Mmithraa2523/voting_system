// Smart Voting System JavaScript

// Authentication failure sound
function playAlertSound() {
    const audio = new Audio('data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1fdJivrJBhNjVgodDbq2EcBj+a2/LDciUFLIHO8tiJNwgZaLvt559NEAxQp+PwtmMcBjiR1/LMeSwFJHfH8N2QQAoUXrTp66hVFApGn+DyvmgbBzuU2vPNeSsFJHfH8N+PQAoUXrPq66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmgbBzyU2vLNeSsFJHfH8N+PQAoTXrTp66pTFAlFn+HyvmigAAABhYXZlTGlzdHMAAAAnYZmCDAIAAAABAIAjCCA=');
    audio.play().catch(console.error);
}

// Authentication failure visual effect
function triggerAuthFailure() {
    const body = document.body;
    body.classList.add('auth-failure');
    playAlertSound();
    
    setTimeout(() => {
        body.classList.remove('auth-failure');
    }, 3000);
}

// Webcam utilities
class WebcamManager {
    constructor() {
        this.stream = null;
        this.video = null;
    }
    
    async startWebcam(videoElement) {
        try {
            this.video = videoElement;
            this.stream = await navigator.mediaDevices.getUserMedia({ 
                video: { 
                    width: 640, 
                    height: 480,
                    facingMode: 'user'
                } 
            });
            this.video.srcObject = this.stream;
            return true;
        } catch (error) {
            console.error('Error accessing webcam:', error);
            return false;
        }
    }
    
    captureFrame() {
        if (!this.video) return null;
        
        const canvas = document.createElement('canvas');
        canvas.width = this.video.videoWidth;
        canvas.height = this.video.videoHeight;
        const ctx = canvas.getContext('2d');
        ctx.drawImage(this.video, 0, 0);
        
        return canvas.toDataURL('image/jpeg', 0.8);
    }
    
    stopWebcam() {
        if (this.stream) {
            this.stream.getTracks().forEach(track => track.stop());
            this.stream = null;
        }
        if (this.video) {
            this.video.srcObject = null;
        }
    }
}

// Form validation utilities
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return false;
    
    const inputs = form.querySelectorAll('input[required], select[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.classList.add('is-invalid');
            isValid = false;
        } else {
            input.classList.remove('is-invalid');
        }
    });
    
    return isValid;
}

// API utilities
async function apiRequest(url, method = 'GET', data = null) {
    const options = {
        method,
        headers: {
            'Content-Type': 'application/json',
        }
    };
    
    if (data) {
        options.body = JSON.stringify(data);
    }
    
    try {
        const response = await fetch(url, options);
        return await response.json();
    } catch (error) {
        console.error('API request failed:', error);
        throw error;
    }
}

// Animation utilities
function animateElement(element, animation, duration = 500) {
    element.style.animation = `${animation} ${duration}ms ease-out`;
    
    setTimeout(() => {
        element.style.animation = '';
    }, duration);
}

// Initialize app
document.addEventListener('DOMContentLoaded', function() {
    // Add smooth scrolling
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Initialize tooltips if Bootstrap is loaded
    if (typeof bootstrap !== 'undefined') {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
    
    // Auto-hide alerts after 5 seconds
    setTimeout(() => {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(alert => {
            if (alert.classList.contains('show')) {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }
        });
    }, 5000);
});

// Export for use in other scripts
window.SmartVoting = {
    WebcamManager,
    triggerAuthFailure,
    playAlertSound,
    validateForm,
    apiRequest,
    animateElement
};