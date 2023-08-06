<?php
class ModelExtensionJadeCustomfooter extends Model {
	public function CreateJadeFooterTable() {
		$this->db->query("CREATE TABLE IF NOT EXISTS `". DB_PREFIX ."jade_customfooter` (`jade_customfooter_id` int(11) NOT NULL AUTO_INCREMENT, `type_code` varchar(255) NOT NULL, `size_class` varchar(255) NOT NULL, `sort_order` int(3) NOT NULL DEFAULT '0', `status` tinyint(1) NOT NULL DEFAULT '1', `contactdetail_table` text NOT NULL, `accountlinks_table` text NOT NULL, `informationlinks_table` text NOT NULL, `sociallinks_table` text NOT NULL, `payments_table` text NOT NULL, `appicons_table` text NOT NULL, `editor_description` text NOT NULL, `newsletter_table` text NOT NULL, PRIMARY KEY (`jade_customfooter_id`)) ENGINE=MyISAM  DEFAULT CHARSET=utf8 AUTO_INCREMENT=0");

		$this->db->query("CREATE TABLE IF NOT EXISTS `". DB_PREFIX ."jade_customfooter_description` (`jade_customfooter_id` int(11) NOT NULL, `language_id` int(11) NOT NULL, `title` varchar(64) NOT NULL, PRIMARY KEY (`jade_customfooter_id`,`language_id`)) ENGINE=MyISAM DEFAULT CHARSET=utf8;");

		$this->db->query("CREATE TABLE IF NOT EXISTS `". DB_PREFIX ."jade_customfooter_newsletter` (`newsletter_id` int(11) NOT NULL AUTO_INCREMENT, `email` varchar(96) NOT NULL, `store_id` int(11) NOT NULL, `language_id` int(11) NOT NULL, `ip` varchar(40) NOT NULL, `status` tinyint(4) NOT NULL, `date_added` datetime NOT NULL, `date_modified` datetime NOT NULL, PRIMARY KEY (`newsletter_id`)) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=0");

		$this->db->query("CREATE TABLE IF NOT EXISTS `". DB_PREFIX ."jade_customfooter_customer_group` (`jade_customfooter_id` int(11) NOT NULL, `customer_group_id` int(11) NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8");

		$this->db->query("CREATE TABLE IF NOT EXISTS `". DB_PREFIX ."jade_customfooter_store` (`jade_customfooter_id` int(11) NOT NULL, `store_id` int(11) NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8");
	}

	public function addJadeCustomfooter($data) {
		$contactdetail_table = (!empty($data['contactdetail_table']) ? json_encode($data['contactdetail_table']) : '');
		$accountlinks_table = (!empty($data['accountlinks_table']) ? json_encode($data['accountlinks_table']) : '');
		$informationlinks_table = (!empty($data['informationlinks_table']) ? json_encode($data['informationlinks_table']) : '');
		$sociallinks_table = (!empty($data['sociallinks_table']) ? json_encode($data['sociallinks_table']) : '');
		$payments_table = (!empty($data['payments_table']) ? json_encode($data['payments_table']) : '');
		$appicons_table = (!empty($data['appicons_table']) ? json_encode($data['appicons_table']) : '');
		$editor_description = (!empty($data['editor_description']) ? json_encode($data['editor_description']) : '');
		$newsletter_table = (!empty($data['newsletter_table']) ? json_encode($data['newsletter_table']) : '');

		$this->db->query("INSERT INTO " . DB_PREFIX . "jade_customfooter SET sort_order = '" . (int)$data['sort_order'] . "', status = '" . (int)$data['status'] . "', type_code = '" . $this->db->escape($data['type_code']) . "', size_class = '" . $this->db->escape($data['size_class']) . "', contactdetail_table = '" . $this->db->escape($contactdetail_table) . "', accountlinks_table = '" . $this->db->escape($accountlinks_table) . "', informationlinks_table = '" . $this->db->escape($informationlinks_table) . "', sociallinks_table = '" . $this->db->escape($sociallinks_table) . "', payments_table = '" . $this->db->escape($payments_table) . "', appicons_table = '" . $this->db->escape($appicons_table) . "', editor_description = '" . $this->db->escape($editor_description) . "', newsletter_table = '" . $this->db->escape($newsletter_table) . "'");

		$jade_customfooter_id = $this->db->getLastId();

		foreach ($data['jade_customfooter_description'] as $language_id => $value) {
			$this->db->query("INSERT INTO " . DB_PREFIX . "jade_customfooter_description SET jade_customfooter_id = '" . (int)$jade_customfooter_id . "', language_id = '" . (int)$language_id . "', title = '" . $this->db->escape($value['title']) . "'");
		}

		if (isset($data['jade_customfooter_store'])) {
			foreach ($data['jade_customfooter_store'] as $store_id) {
				$this->db->query("INSERT INTO " . DB_PREFIX . "jade_customfooter_store SET jade_customfooter_id = '" . (int)$jade_customfooter_id . "', store_id = '" . (int)$store_id . "'");
			}
		}

		if (isset($data['jade_customfooter_customer_group'])) {
			foreach ($data['jade_customfooter_customer_group'] as $customer_group_id) {
				$this->db->query("INSERT INTO " . DB_PREFIX . "jade_customfooter_customer_group SET jade_customfooter_id = '" . (int)$jade_customfooter_id . "', customer_group_id = '" . (int)$customer_group_id . "'");
			}
		}

		return $jade_customfooter_id;
	}

	public function editJadeCustomfooter($jade_customfooter_id, $data) {
		$contactdetail_table = (!empty($data['contactdetail_table']) ? json_encode($data['contactdetail_table']) : '');
		$accountlinks_table = (!empty($data['accountlinks_table']) ? json_encode($data['accountlinks_table']) : '');
		$informationlinks_table = (!empty($data['informationlinks_table']) ? json_encode($data['informationlinks_table']) : '');
		$sociallinks_table = (!empty($data['sociallinks_table']) ? json_encode($data['sociallinks_table']) : '');
		$payments_table = (!empty($data['payments_table']) ? json_encode($data['payments_table']) : '');
		$appicons_table = (!empty($data['appicons_table']) ? json_encode($data['appicons_table']) : '');
		$editor_description = (!empty($data['editor_description']) ? json_encode($data['editor_description']) : '');
		$newsletter_table = (!empty($data['newsletter_table']) ? json_encode($data['newsletter_table']) : '');

		$this->db->query("UPDATE " . DB_PREFIX . "jade_customfooter SET sort_order = '" . (int)$data['sort_order'] . "', status = '" . (int)$data['status'] . "', type_code = '" . $this->db->escape($data['type_code']) . "', size_class = '" . $this->db->escape($data['size_class']) . "', contactdetail_table = '" . $this->db->escape($contactdetail_table) . "', accountlinks_table = '" . $this->db->escape($accountlinks_table) . "', informationlinks_table = '" . $this->db->escape($informationlinks_table) . "', sociallinks_table = '" . $this->db->escape($sociallinks_table) . "', payments_table = '" . $this->db->escape($payments_table) . "', appicons_table = '" . $this->db->escape($appicons_table) . "', editor_description = '" . $this->db->escape($editor_description) . "', newsletter_table = '" . $this->db->escape($newsletter_table) . "' WHERE jade_customfooter_id = '" . (int)$jade_customfooter_id . "'");

		$this->db->query("DELETE FROM " . DB_PREFIX . "jade_customfooter_description WHERE jade_customfooter_id = '" . (int)$jade_customfooter_id . "'");

		foreach ($data['jade_customfooter_description'] as $language_id => $value) {
			$this->db->query("INSERT INTO " . DB_PREFIX . "jade_customfooter_description SET jade_customfooter_id = '" . (int)$jade_customfooter_id . "', language_id = '" . (int)$language_id . "', title = '" . $this->db->escape($value['title']) . "'");
		}

		$this->db->query("DELETE FROM " . DB_PREFIX . "jade_customfooter_store WHERE jade_customfooter_id = '" . (int)$jade_customfooter_id . "'");

		if (isset($data['jade_customfooter_store'])) {
			foreach ($data['jade_customfooter_store'] as $store_id) {
				$this->db->query("INSERT INTO " . DB_PREFIX . "jade_customfooter_store SET jade_customfooter_id = '" . (int)$jade_customfooter_id . "', store_id = '" . (int)$store_id . "'");
			}
		}

		$this->db->query("DELETE FROM " . DB_PREFIX . "jade_customfooter_customer_group WHERE jade_customfooter_id = '" . (int)$jade_customfooter_id . "'");

		if (isset($data['jade_customfooter_customer_group'])) {
			foreach ($data['jade_customfooter_customer_group'] as $customer_group_id) {
				$this->db->query("INSERT INTO " . DB_PREFIX . "jade_customfooter_customer_group SET jade_customfooter_id = '" . (int)$jade_customfooter_id . "', customer_group_id = '" . (int)$customer_group_id . "'");
			}
		}
	}

	public function deleteJadeCustomfooter($jade_customfooter_id) {
		$this->db->query("DELETE FROM " . DB_PREFIX . "jade_customfooter WHERE jade_customfooter_id = '" . (int)$jade_customfooter_id . "'");
		$this->db->query("DELETE FROM " . DB_PREFIX . "jade_customfooter_description WHERE jade_customfooter_id = '" . (int)$jade_customfooter_id . "'");
	}

	public function getJadeCustomfooter($jade_customfooter_id) {
		$query = $this->db->query("SELECT DISTINCT * FROM " . DB_PREFIX . "jade_customfooter WHERE jade_customfooter_id = '" . (int)$jade_customfooter_id . "'");

		return $query->row;
	}

	public function getJadeCustomfooters($data = array()) {
		$sql = "SELECT * FROM " . DB_PREFIX . "jade_customfooter jc LEFT JOIN " . DB_PREFIX . "jade_customfooter_description jcd ON (jc.jade_customfooter_id = jcd.jade_customfooter_id) WHERE jcd.language_id = '" . (int)$this->config->get('config_language_id') . "'";

		$sort_data = array(
			'jcd.title',
			'jc.sort_order'
		);

		if (isset($data['sort']) && in_array($data['sort'], $sort_data)) {
			$sql .= " ORDER BY " . $data['sort'];
		} else {
			$sql .= " ORDER BY jcd.title";
		}

		if (isset($data['order']) && ($data['order'] == 'DESC')) {
			$sql .= " DESC";
		} else {
			$sql .= " ASC";
		}

		if (isset($data['start']) || isset($data['limit'])) {
			if ($data['start'] < 0) {
				$data['start'] = 0;
			}

			if ($data['limit'] < 1) {
				$data['limit'] = 20;
			}

			$sql .= " LIMIT " . (int)$data['start'] . "," . (int)$data['limit'];
		}

		$query = $this->db->query($sql);

		return $query->rows;
	}

	public function getJadeCustomfooterDescriptions($jade_customfooter_id) {
		$jade_customfooter_description_data = array();

		$query = $this->db->query("SELECT * FROM " . DB_PREFIX . "jade_customfooter_description WHERE jade_customfooter_id = '" . (int)$jade_customfooter_id . "'");

		foreach ($query->rows as $result) {
			$jade_customfooter_description_data[$result['language_id']] = array(
				'title'            => $result['title'],
			);
		}

		return $jade_customfooter_description_data;
	}

	public function getTotalJadeCustomfooters() {
		$query = $this->db->query("SELECT COUNT(*) AS total FROM " . DB_PREFIX . "jade_customfooter");

		return $query->row['total'];
	}

	public function getFooterStores($jade_customfooter_id) {
		$customfooter_store_data = array();

		$query = $this->db->query("SELECT * FROM " . DB_PREFIX . "jade_customfooter_store WHERE jade_customfooter_id = '" . (int)$jade_customfooter_id . "'");

		foreach ($query->rows as $result) {
			$customfooter_store_data[] = $result['store_id'];
		}

		return $customfooter_store_data;
	}

	public function getFooterCustomerGroups($jade_customfooter_id) {
		$customfooter_customer_group_data = array();

		$query = $this->db->query("SELECT * FROM " . DB_PREFIX . "jade_customfooter_customer_group WHERE jade_customfooter_id = '" . (int)$jade_customfooter_id . "'");

		foreach ($query->rows as $result) {
			$customfooter_customer_group_data[] = $result['customer_group_id'];
		}

		return $customfooter_customer_group_data;
	}
}