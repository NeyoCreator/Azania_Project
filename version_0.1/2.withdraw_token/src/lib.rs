use scrypto::prelude::*;

blueprint! {
    struct TokenMachine {
        dinar_vault: Vault,
        collected_xrd: Vault,
        price: Decimal
    }

    impl TokenMachine {
        // We are returning a bucket containing the admin badge along with the
        pub fn instantiate_machine(price: Decimal) -> (ComponentAddress, Bucket) {
            // CREATE ADMIN BADGE
            let admin_badge: Bucket = ResourceBuilder:: new_fungible()
                .divisibility(DIVISIBILITY_NONE)
                .metadata("name", "Token Machine Admin ")
                .initial_supply(1);
            
            // Create a new dinar resource
            let dinar_vault: Bucket = ResourceBuilder::new_fungible()
                .divisibility(DIVISIBILITY_NONE)
                .metadata("name", "Dinars")
                .metadata("symbol", "DNH")
                .initial_supply(500);

            // AUTHENTICATION
            let access_rule = AccessRules::new()
                .method("withdraw_xrd",rule!(require(admin_badge.resource_address())))
                .default(rule!(allow_all));

            // INSTATIATE COMPONENT 
            let component = Self{
                dinar_vault: Vault::with_bucket(dinar_vault),
                collected_xrd: Vault::new(RADIX_TOKEN),
                price:price

            }
            .instantiate()
            .add_access_check(access_rule);

            // RETURN COMPONENT AND BADGE
            (component.globalize(), admin_badge)

        }

        // Allow users to buy a dinar by providing enough XRD.
        // Returns a single dinar and the remaining of the payment bucket (the change)
        pub fn buy_dinar(&mut self, mut payment: Bucket) -> (Bucket, Bucket) {
            let our_share = payment.take(self.price);
            self.collected_xrd.put(our_share);

            let dinar: Bucket = self.dinar_vault.take(1);
            (dinar, payment)
            
        }

        pub fn withdraw_xrd(&mut self) -> Bucket {
            // Simply take all resources from the collected_xrd vault and
            // return them
            self.collected_xrd.take_all()
        }


    }
}
