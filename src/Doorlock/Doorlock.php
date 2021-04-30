<?php

namespace App\Doorlock;

/**
 * @author František Hrdý
 * @author Martin Růžek
 */
class Doorlock
{
    /**
     * @var string
     */
    private $lockUrl;

    /**
     * @var string
     */
    private $lockAuthenticationKey;

    /**
     * @param string $lockUrl
     * @param string $lockAuthenticationKey
     */
    public function __construct(string $lockUrl, string $lockAuthenticationKey)
    {
        $this->lockUrl = $lockUrl;
        $this->lockAuthenticationKey = $lockAuthenticationKey;
    }

    public function unlock(): void
    {

    }

    public function getStatus(): array
    {
        $lockAuthenticationKey = base64_encode($this->lockAuthenticationKey);
        $context = stream_context_create([
            'http' => [
                'header' => 'Authorization: Basic ' . $lockAuthenticationKey
            ]
        ]);
        $rawStatus = @file_get_contents($this->lockUrl, false, $context);
        if ($rawStatus === false) {
            throw new Exception('An attempt to retrieve lock status failed.');
        }
        // Example: $rawStatus = 'true-600' | $rawStatus = 'false-null'
        $status = explode('-', $rawStatus);

        $finalStatus = [];

        if ($status[0] === 'true') {
            $finalStatus['state'] = true;
            $finalStatus['timeToLock'] = (int)$status[1];
        } else {
            $finalStatus['state'] = false;
            $finalStatus['timeToLock'] = null;
        }
            
        return $finalStatus;
    }
}
